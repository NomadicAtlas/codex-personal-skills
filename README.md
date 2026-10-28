# Codex Personal Skills Backup

Portable source backup of six current personal skills, captured on **2026-10-28**
(Asia/Shanghai). The installed source snapshot is recorded in [skills.json](skills.json).
Each directory is a separate skill. The combined repository and ZIP are distribution
containers, not a single installable skill.

## Inventory

| Skill | Purpose and invocation | Edition / dependencies |
|---|---|---|
| [`academic-research-suite`](skills/academic-research-suite/) | Academic research, evidence synthesis, qualitative analysis, theory, writing, review and revision | Current **Online Edition**, shown as ARS-Codex Lite; adapted from ARS-Codex 0.1.25 |
| [`research-clarifier`](skills/research-clarifier/) | Resolve consequential research uncertainty; reuse settled context and avoid duplicate intake | Personal skill |
| [`bilingual-humanizer`](skills/bilingual-humanizer/) | Preserve claims and citations while revising Chinese, English or mixed prose | Explicit request or explicitly selected workflow only |
| [`scientific-visualization`](skills/scientific-visualization/) | Scientific figures, conceptual diagrams, accessibility and export checks | Select the required installed Python tools; verify journal rules for targeted submission |
| [`pptx-posters`](skills/pptx-posters/) | Editable scientific poster drafts, content review and separate print-release preparation | Draft and strict print-release paths have different requirements; preserve all scripts, assets and references |
| [`zotero-research-workflow`](skills/zotero-research-workflow/) | Zotero source identity, supporting passages and manuscript evidence | Companion to available Zotero tools or supplied bibliographic/source files; does not install Zotero |

Total current skills: **6**. This snapshot has **75 skill files**, excluding runtime
caches. The exact file inventory, modes, sizes, per-file SHA-256 and per-skill tree
SHA-256 are in [skills.json](skills.json).

## Current source and portable package

- Browse and review the current source under [skills/](skills/).
- Download and extract [codex-personal-skills-bundle.zip](codex-personal-skills-bundle.zip).
- Run `python3 scripts/backup.py verify` in a repository checkout.
- Run `sha256sum -c SHA256SUMS` to check the distribution and preserved historical files.
- After extracting only the ZIP, run `sha256sum -c FILE_SHA256SUMS` in its root to
  check all 75 skill files. On macOS, use `shasum -a 256 -c FILE_SHA256SUMS`.

The ZIP contains the same README, skills.json, CHANGELOG and FILE_SHA256SUMS as the
repository, together with the six complete skill directories. The distribution
[SHA256SUMS](SHA256SUMS) is kept outside the ZIP so the package never contains its
own final hash. Repository-only links such as archives/ and scripts/ are available
from this GitHub repository, not from the extracted ZIP.

## Restore the selected skill

**Filesystem-based Codex environment:** select a directory under skills/ and
restore that complete directory into the personal-skill location configured by
the target client. Keep SKILL.md, agents/, references/, assets/, scripts/, tests
and license files together wherever present. The destination is client-specific;
do not assume that the managed ChatGPT checkout and a local Codex directory use
the same installation path.

**ChatGPT managed personal skills:** ask the available skill-creator workflow to
import/install the selected individual skill from its directory or an individual
package. That workflow handles validation and saving to the managed skill
directory. Copying files on a local computer does not update a managed ChatGPT
skill. Do not import the combined six-skill backup as one skill.

Refresh the target client's Skills page, or use a new conversation if its skill
list is cached. Restore only the edition intended for that environment.

Zotero operations require an actual available connector or a host that can reach
the user's Zotero Desktop. A cloud host's localhost is not the user's computer.
The companion can work from supplied bibliographic exports and accessible source
material when a desktop connection is unavailable.

## Historical August backup

The original three-skill backup is preserved byte for byte under
[archives/2026-08-15/](archives/2026-08-15/), with its original README, skills.json,
ZIP and an [archive record](archives/2026-08-15/archive.json).
The original commit was dated 2026-08-14 18:11:35 UTC, which is
2026-08-15 02:11:35 in Asia/Shanghai.

The historical ARS is the **full desktop distribution** (2,259 files), with
adapter version 0.1.25 and upstream suite 3.20.0 recorded in its own manifest.
The current 12-file Online Edition is a separate personal adaptation. Keep these
editions separate; overlaying a new router onto the old full directory would not
reproduce the installed Online Edition.

Known historical issues are retained in archive.json: the full ARS manifest
points to a missing VERSION file, and the ZIP's internal README differs from
the original repository README. No historical file has been silently repaired.

Original ZIP SHA-256:

`AA7E48CE21F5C9D2B2EA2D87F7CEA09FD7F9063B0BCCC8399212B8BEEC93050E`

## Update this backup

1. Locate the intended installed skills by each SKILL.md name. Record the source
   snapshot and inspect pending changes before exporting.
2. Export each complete directory to skills/<name>/, preserving file bytes,
   executable modes, attribution and license files. Exclude __pycache__, *.pyc,
   .pytest_cache, .venv and repository internals. Do not rewrite skill behavior
   merely to refresh this backup.
3. Update this inventory and skills.json metadata: generation date/time,
   source_snapshot_commit, per-skill local_revision, edition, upstream version
   where known, and source attribution. A local revision date is not an upstream
   release version. Keep generated_at in the stated timezone.
4. Add a dated entry to the root CHANGELOG. Validate the actual installed skills
   with the current skill-creator validator; keep packaging checks distinct from
   behavioral, rendering and print-release checks.
5. Run `python3 scripts/backup.py build`, then `python3 scripts/backup.py verify`.
   The builder refreshes file records, both checksum lists and the ZIP. ZIP
   metadata and file order are fixed for deterministic rebuilds with unchanged
   inputs in the same compression environment.
6. Review the source and metadata diff, verify historical hashes, and submit the
   update branch. Leave the historical August archive unchanged.

The builder uses the Python standard library and does not install dependencies,
execute skill scripts, access Zotero or certify scientific/print quality.
It refuses inconsistent skill names, missing explicit resources, changed
historical files, and divergent package contents.

## Provenance and validation scope

[CHANGELOG.md](CHANGELOG.md) records the August additions, September refinements
and October changes. Skills retain their own notices and license files. ARS
attribution and CC BY-NC 4.0 terms are retained in its directory; Bilingual
Humanizer retains its MIT attribution; the visualization and poster skills retain
K-Dense Inc. MIT notices. There is no new blanket license replacing these terms.

This update checks snapshot identity, the six installed skills' structural
validation, source-to-package equality, historical byte preservation, deterministic
rebuilds and checksums. It does not claim a new end-to-end execution of every skill,
Chinese font/rendering validation, PowerPoint review, accessibility certification
or approval for print.
