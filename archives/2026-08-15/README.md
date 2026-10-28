# Codex Personal Skills Backup

Personal backup of Codex skills for reuse across computers.

## Inventory

| Skill | Purpose | Source |
|---|---|---|
| `academic-research-suite` | Academic research, writing, review, and experiment workflows | https://github.com/Imbad0202/academic-research-skills-codex |
| `research-clarifier` | Clarify complex research problems before proposing solutions | Locally authored personal skill |
| `bilingual-humanizer` | Humanize Chinese, English, or mixed-language prose while preserving claims and citations | Local ZIP package |

Total personal skills in this backup: **3**.

## Backup package

The complete contents of all three skills are stored in:

```text
codex-personal-skills-bundle.zip
```

SHA-256:

```text
AA7E48CE21F5C9D2B2EA2D87F7CEA09FD7F9063B0BCCC8399212B8BEEC93050E
```

## Restore

Download and extract `codex-personal-skills-bundle.zip`, then copy the desired folder from its `skills/` directory into the target computer's Codex user skill directory:

```text
$CODEX_HOME/skills/<skill-name>
```

When `CODEX_HOME` is unset, use the user-level Codex skills directory configured on that computer. Open a new Codex conversation after restoring so the skill list refreshes.

## Update this backup

Rebuild `codex-personal-skills-bundle.zip`, update `skills.json` and the SHA-256 value above, then commit and push. Keep each skill directory inside the archive self-contained, including its `SKILL.md`, `agents/`, references, assets, scripts, and license files.

## Notes

- This repository is intended as a portable backup and inventory, not as a single combined skill.
- Preserve upstream license and attribution files.
- Review private or sensitive reference materials before making the repository public.
