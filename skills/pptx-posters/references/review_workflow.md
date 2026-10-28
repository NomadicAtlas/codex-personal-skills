# Draft and content-final poster workflow

Use this lightweight schema with `scripts/generate_review_poster.py`; do not pass it to the strict 2.0 release generator. Default to draft and preserve real supplied content. Do not manufacture sources or approval to satisfy the schema.

Required top-level keys: `schema_version: "review-1.0"`, `title`, `width_in`, `height_in`, `language`, `elements`, `pending_content`, `pending_production`, and `reviewed_by` (null until genuinely reviewed). Canvas size is a provisional design size, not a confirmed printer trim size. Record this in pending production when applicable.

Each element requires `type`, `x_in`, `y_in`, `width_in`, `height_in`, and `source`. Source is a real supplied locator/description or null; null adds a pending content item. Text elements also require `text`, `font_face`, `font_size_pt`, and boolean `bold`. Image elements instead require manifest-relative `path`, actual `sha256`, and `alt_text`; only local PNG/JPEG files within the manifest directory are accepted. The first element must be title text matching `title` exactly. Reserve the bottom 0.45 inches for the automatic review status. Arrays of pending items contain actual unresolved questions, not fabricated claims.

Run:

```bash
python -B scripts/generate_review_poster.py review.json --output poster-draft.pptx --report poster-draft.json
python -B scripts/generate_review_poster.py review.json --stage content-final --output poster-content-final.pptx --report poster-content-final.json
```

Content-final requires an actual reviewer, an empty pending-content list, and sources for every element. This records content review; it does not verify the science or authorize external publication. Production questions may remain unresolved. Layout-only changes can be generated again to a new file without a fresh scientific approval; check visual rendering after each layout change.

The generator rejects unsafe paths, changed image hashes, hidden image metadata, remote assets, macros, external relationships, and overwrites. It reports layout issues without preventing draft review. It also reports local font-family substitution and missing glyphs when Fontconfig/fontTools are available; otherwise font coverage remains explicitly unverified. A missing-glyph or substituted-font report requires visual resolution before claiming the draft renders correctly. Inspect the report and render the PPTX using an available presentation renderer before delivery; fix avoidable clipping, overflow, and illegibility. Report actual renderer limitations. A clean package check or layout report is not accessibility certification.

For print release, assemble the existing strict 2.0 manifest from genuinely confirmed requirements, content, assets, and final production choices; obtain the real final sign-off and run all release checks. Do not auto-promote review metadata into approval fields. Use the presentation/PDF skills for rendering and export as needed; opening a generated clean file for rendering is not forbidden by the release rule against executing untrusted templates.
