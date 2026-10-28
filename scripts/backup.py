#!/usr/bin/env python3
"""Build or verify the portable skill snapshot using only the Python standard library."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import zipfile

BUNDLE = "codex-personal-skills-bundle.zip"
ARCHIVE = "archives/2026-08-15"
DOCUMENTS = ["README.md", "skills.json", "CHANGELOG.md", "FILE_SHA256SUMS"]
IGNORED = {".git", ".venv", "__pycache__", ".pytest_cache"}
ORIGINAL_ZIP_SHA256 = "aa7e48ce21f5c9d2b2ea2d87f7cea09fd7f9063b0bccc8399212b8beec93050e"
ORIGINAL_BLOBS = {
    "README.md": "c54a318f191028bf4d4413e9a53c1af3b29747ee",
    "skills.json": "4e6754c59c701609badf8aa913f39ace10e29939",
    BUNDLE: "c751acb3660009c80062bbfad25c2aa5ba37d3a3",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write(path: Path, data: bytes) -> None:
    temporary = path.with_name(path.name + ".tmp")
    try:
        temporary.write_bytes(data)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def skill_state(root: Path, record: dict) -> dict:
    name = record["name"]
    require(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) is not None, f"Invalid name: {name}")
    require(record["path"] == f"skills/{name}", f"Unexpected source path: {name}")
    folder = root / record["path"]
    require(folder.is_dir() and not folder.is_symlink(), f"Missing/linked skill directory: {name}")
    entrypoint = folder / "SKILL.md"
    require(entrypoint.is_file(), f"Missing SKILL.md: {name}")
    text = entrypoint.read_text(encoding="utf-8")
    require(text.startswith("---\n"), f"Missing frontmatter: {name}")
    frontmatter = text.split("---", 2)[1]
    match = re.search(r"^name:\s*(\S+)\s*$", frontmatter, re.M)
    require(match is not None and match.group(1) == name, f"Frontmatter name mismatch: {name}")
    for reference in set(re.findall(r"(?:references|assets|scripts)/[A-Za-z0-9_.-]+", text)):
        require((folder / reference).exists(), f"Missing referenced resource: {name}/{reference}")
    ui = folder / "agents/openai.yaml"
    require(ui.is_file(), f"Missing UI metadata: {name}")
    for match in re.finditer(r"^\s*icon_(?:small|large):\s*(.+?)\s*$", ui.read_text(), re.M):
        icon = match.group(1).strip("'\"")
        require((folder / icon).is_file(), f"Missing icon: {name}/{icon}")
    for license_path in record.get("license_files", []):
        require((folder / license_path).is_file(), f"Missing license: {name}/{license_path}")
    files = []
    for file in sorted(folder.rglob("*")):
        relative = file.relative_to(folder)
        if any(part in IGNORED for part in relative.parts) or file.suffix == ".pyc":
            continue
        require(not file.is_symlink(), f"Symlink is not a portable file: {file}")
        if not file.is_file():
            continue
        data = file.read_bytes()
        files.append({
            "path": relative.as_posix(),
            "sha256": sha256(data),
            "bytes": len(data),
            "mode": "100755" if file.stat().st_mode & 0o111 else "100644",
        })
    tree = "".join(f'{file["mode"]} {file["sha256"]}  {file["path"]}\n' for file in files)
    return {
        "file_count": len(files),
        "total_bytes": sum(file["bytes"] for file in files),
        "tree_sha256": sha256(tree.encode()),
        "files": files,
    }


def inventory(root: Path, metadata: dict) -> list[tuple[dict, dict]]:
    require(metadata.get("schema_version") == 2, "Expected manifest schema_version 2")
    records = metadata["skills"]
    names = [record["name"] for record in records]
    require(len(names) == len(set(names)), "Duplicate skill names")
    directories = {file.name for file in (root / "skills").iterdir() if file.is_dir()}
    require(directories == set(names), "Source directories and manifest names differ")
    readme = (root / "README.md").read_text()
    readme_names = re.findall(r"^\| \[\x60([a-z0-9-]+)\x60\]", readme, re.M)
    require(sorted(readme_names) == sorted(names), "README inventory and manifest names differ")
    count = re.search(r"Total current skills: \*\*(\d+)\*\*", readme)
    require(count is not None and int(count.group(1)) == len(names), "README skill count differs")
    require(metadata["generated_at"].startswith(metadata["generated_on"] + "T"), "Snapshot dates differ")
    return [(record, skill_state(root, record)) for record in records]


def source_paths(states: list[tuple[dict, dict]]) -> list[str]:
    return sorted(f'{record["path"]}/{file["path"]}' for record, state in states for file in state["files"])


def sums(root: Path, paths: list[str]) -> bytes:
    return "".join(f"{sha256((root / path).read_bytes())}  {path}\n" for path in sorted(paths)).encode()


def verify_history(root: Path) -> None:
    history = root / ARCHIVE
    record = json.loads((history / "archive.json").read_text())
    require(record["original_commit"] == "ba6807c7c9d3c34ad7089e65e0d1997d82ac81ae", "Historical baseline changed")
    for name, expected_blob in ORIGINAL_BLOBS.items():
        data = (history / name).read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        require(blob == expected_blob, f"Historical file changed: {name}")
        require(record["files"][name]["git_blob_sha"] == expected_blob, f"Historical record differs: {name}")
        require(record["files"][name]["sha256"] == sha256(data), f"Historical hash differs: {name}")
    require(sha256((history / BUNDLE).read_bytes()) == ORIGINAL_ZIP_SHA256, "Historical ZIP changed")


def zip_bytes(root: Path, paths: list[str], generated_on: str) -> bytes:
    year, month, day = map(int, generated_on.split("-"))
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(paths):
            file = root / path
            entry = zipfile.ZipInfo(path, (year, month, day, 0, 0, 0))
            entry.create_system = 3
            mode = 0o755 if file.stat().st_mode & 0o111 else 0o644
            entry.external_attr = (0o100000 | mode) << 16
            archive.writestr(entry, file.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return output.getvalue()


def all_paths(root: Path, paths: list[str]) -> list[str]:
    history = sorted(file.relative_to(root).as_posix() for file in (root / ARCHIVE).iterdir() if file.is_file())
    return sorted(set(paths + DOCUMENTS + ["scripts/backup.py", BUNDLE] + history))


def build(root: Path) -> None:
    metadata = json.loads((root / "skills.json").read_text())
    verify_history(root)
    states = inventory(root, metadata)
    for record, state in states:
        record.update(state)
    metadata["skill_count"] = len(states)
    metadata["total_skill_files"] = sum(state["file_count"] for _, state in states)
    metadata["total_skill_bytes"] = sum(state["total_bytes"] for _, state in states)
    write(root / "skills.json", json_bytes(metadata))
    paths = source_paths(states)
    write(root / "FILE_SHA256SUMS", sums(root, paths))
    write(root / BUNDLE, zip_bytes(root, paths + DOCUMENTS, metadata["generated_on"]))
    write(root / "SHA256SUMS", sums(root, all_paths(root, paths)))
    verify(root)


def verify(root: Path) -> None:
    metadata = json.loads((root / "skills.json").read_text())
    verify_history(root)
    states = inventory(root, metadata)
    require(metadata["skill_count"] == len(states), "Manifest skill count differs")
    require(metadata["total_skill_files"] == sum(state["file_count"] for _, state in states), "Manifest file count differs")
    require(metadata["total_skill_bytes"] == sum(state["total_bytes"] for _, state in states), "Manifest byte count differs")
    for record, state in states:
        for key, value in state.items():
            require(record.get(key) == value, f"Manifest {key} differs: {record['name']}")
    paths = source_paths(states)
    require((root / "FILE_SHA256SUMS").read_bytes() == sums(root, paths), "Per-file checksums differ")
    expected = set(paths + DOCUMENTS)
    with zipfile.ZipFile(root / BUNDLE) as archive:
        require(len(archive.namelist()) == len(set(archive.namelist())), "Duplicate ZIP entries")
        require(set(archive.namelist()) == expected, "ZIP inventory differs")
        require(archive.testzip() is None, "ZIP CRC check failed")
        for path in sorted(expected):
            require(archive.read(path) == (root / path).read_bytes(), f"Decompressed file differs: {path}")
    require((root / BUNDLE).read_bytes() == zip_bytes(root, sorted(expected), metadata["generated_on"]), "ZIP is not the deterministic source build")
    require((root / "SHA256SUMS").read_bytes() == sums(root, all_paths(root, paths)), "Distribution checksums differ")
    print(f'PASS: {len(states)} skills; {metadata["total_skill_files"]} files; {metadata["total_skill_bytes"]} bytes')
    print(f'ZIP SHA-256: {sha256((root / BUNDLE).read_bytes())}')
    print("Historical bytes, metadata, resources, ZIP CRC, decompressed bytes, and checksums verified.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["build", "verify"])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        (build if args.command == "build" else verify)(args.root.resolve())
    except (ValueError, KeyError, OSError, zipfile.BadZipFile) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
