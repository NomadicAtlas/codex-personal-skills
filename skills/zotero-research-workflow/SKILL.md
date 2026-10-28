---
name: zotero-research-workflow
description: Coordinate source verification and manuscript evidence with an explicitly requested Zotero library task, including searching library items, checking supporting passages, and exporting citations. Use when the user asks to work with Zotero or an already established Zotero task. Do not trigger merely for generic citations, reference formatting, or literature discussion.
---

# Zotero research workflow

Use this companion to the installed Zotero plugin. Keep plugin-owned files unchanged; add research judgment and environment routing here. It does not install Zotero or expose new connector capabilities.

## Choose a real execution route

Prefer an exposed Zotero-specific tool when available for the requested operation. Otherwise read the installed Zotero skill and resolve its actual helper path. Check whether the execution host can reach the user's Zotero Desktop before running local commands; localhost on a cloud host is not the user's computer. Never assume a helper file implies access to a desktop session.

On a reachable desktop host, use the plugin's `status --json` first and follow its helper workflow. Do not enable/restart Zotero merely for generic reference checking. On a cloud host without a working connector, explain the specific limitation and continue from user-supplied BibTeX/RIS/CSL JSON or accessible source material. Do not silently switch to unrelated account or browser access.

## Distinguish identity from support

Record title, authors, year, stable identifier, Zotero item key, and citation key where available. Distinguish Zotero keys from exported BibTeX keys. Resolve ambiguous records by bibliographic evidence; never pick one solely because it matches a keyword.

A record in Zotero establishes library identity, not full-text access, research quality, or support for a manuscript claim. For claim verification, identify the exact proposition and inspect the relevant passage when access is authorized. A user request to read or verify supporting passages authorizes the necessary full-text retrieval under the plugin's rules. Do not retrieve unrelated attachments.

Use `references/claim-check.md` for claim-level audits. Keep unread, abstract-only, partly read, and verified-passage states distinct. Preserve page/section locators and quotation wording. Do not invent DOI, pages, citation keys, findings, or evidence of having read a source.

## Writes and outputs

Follow the plugin's write boundaries. An explicit request to import/add specified records authorizes that import; do not ask again for already specified actions. Resolve ambiguous destination or records before dependent writes. Preserve existing citation fields and keys in manuscript files. Use Library for user-facing exports when applicable; saving a file does not itself import it into Zotero.

Return concise results and material access limitations. Do not report successful library operations, claim verification, or citation synchronization unless the relevant action actually succeeded.
