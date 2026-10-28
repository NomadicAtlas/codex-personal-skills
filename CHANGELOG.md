# Backup changelog

Dates use Asia/Shanghai. Historical entries describe observed installed-source
history; they do not imply that GitHub was updated on those dates.

## 2026-10-28 — Six-skill current snapshot

- Exported the six current personal skills from source snapshot
  26ca5ff629fc007dadb5f507ad1129ddede23d56: 75 skill files, 549,787 bytes.
- Added the previously unbacked scientific-visualization, pptx-posters and
  zotero-research-workflow directories.
- Synced current Research Clarifier and Bilingual Humanizer revisions and the
  complete 12-file ARS Online Edition.
- Preserved the original three-skill full backup from commit
  ba6807c7c9d3c34ad7089e65e0d1997d82ac81ae under archives/2026-08-15/.
- Recorded the historical full ARS missing VERSION reference and the old package
  README difference without altering the original archive.
- Added schema-2 source/edition/revision metadata, per-file hashes, separate
  distribution checksums, and a deterministic build/verification script.
- Validation for this backup: current canonical skill structure, source byte and
  mode equality, archive preservation, ZIP CRC/decompressed equality, checksum
  consistency, repeated-build equality, and tampering detection.
- Behavioral outputs, Chinese font/rendering, PowerPoint and print-release
  validation have not been repeated as part of this packaging update.

## 2026-10-19 — Five refinements and Zotero companion

- Academic Research Suite: strengthened qualitative analysis and manuscript
  revision workflows; added qualitative-analysis.md, theory-contribution.md and
  revision-continuity.md; updated writing/design references and skill coordination.
- Research Clarifier: clarified its handoff to the main scholarly workflow.
- Bilingual Humanizer: aligned explicit invocation and embedded-workflow boundaries.
- Scientific Visualization: added runtime selection and conceptual-figure guidance.
- PPTX Posters: added draft/content-final generation and review workflow, repaired
  rendering namespaces, and added review-generator tests while retaining strict
  print-release gates.
- Added Zotero Research Workflow with claim-support verification and environment
  routing. Bibliographic identity remains separate from having read a supporting
  passage.

## 2026-09-12 — Scoped research and writing workflows

- Research Clarifier: removed the numerical 95% stopping target and repeated
  clarification barriers; continued independent work where feasible.
- Academic Research Suite: reused established questions, constraints and evidence
  boundaries instead of repeating intake.
- Bilingual Humanizer: added lightweight editing for short, straightforward text.
- Scientific Visualization: scoped live publisher checks to the requested figure
  destination; retained official-guideline checks for actual submission.

## 2026-08-16 — Two installed skills added

- Installed Scientific Visualization and PPTX Posters in the personal skill set.
- These installations were absent from the original three-skill GitHub backup.

## 2026-08-15 — Original portable backup

- Repository initialization: 5703ff6b43de4b922cf24f798470b92241fa3136.
- Original portable package: ba6807c7c9d3c34ad7089e65e0d1997d82ac81ae.
- Included the full Academic Research Suite distribution, Research Clarifier and
  Bilingual Humanizer. The current managed ARS Online Edition is a distinct
  distribution.
- UTC timestamps were on August 14; local backup metadata used August 15.
