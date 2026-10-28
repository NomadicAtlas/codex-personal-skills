---
name: bilingual-humanizer
description: Revise Chinese, English, or mixed-language prose so it reads naturally and avoids formulaic AI-writing patterns while preserving meaning, evidence, citations, quotations, terminology, and register. Use only when the user explicitly invokes $bilingual-humanizer, directly asks to use Bilingual Humanizer, or explicitly selects a workflow that names this skill as its prose pass. Do not activate merely because the task involves academic editing or generic polishing. Supports academic, professional, technical, and general writing; it does not claim to detect AI authorship or guarantee detector outcomes.
---

# Bilingual Humanizer

Edit prose in Chinese, English, or both. Improve human voice and rhetorical control without changing the author's intellectual position.

## Route by language and context

1. Detect the language of each passage. For mixed text, treat Chinese and English spans separately while preserving cross-language terminology.
2. Infer the register from the text and request: academic, professional, technical, general, personal, or literary.
3. If the register is academic or the text contains citations, quotations, methods, findings, theory, or participant speech, read [academic-guardrails.md](references/academic-guardrails.md) before editing.
4. In the full editing mode, read [english-patterns.md](references/english-patterns.md) for English spans and [chinese-patterns.md](references/chinese-patterns.md) for Chinese spans. For mixed text, read both.
5. Apply only patterns actually present. Diagnose clusters, not isolated words or punctuation.

## Non-negotiable constraints

- Preserve every substantive claim, qualification, causal relation, comparison, limitation, name, number, date, citation, quotation, and source attribution unless the user explicitly authorizes substantive editing.
- Preserve propositions, not their rhetorical shell. Re-express inflated or formulaic wording while keeping the same claim strength; do not retain stock phrasing merely because deleting it would weaken the claim.
- Never invent facts, examples, evidence, sources, quotations, citations, page numbers, participant characteristics, methods, findings, or theoretical claims.
- Do not add a plausible intermediate interpretation, mechanism, emotion, or implication that the source leaves unstated, even when a quotation appears to support it.
- Do not turn uncertainty into certainty. Retain justified epistemic caution such as “可能”, “表明”, “suggests”, “may”, and “appears” when it carries methodological meaning.
- Preserve technical terms and defined concepts. Prefer consistent repetition of the correct term over decorative synonym cycling.
- Do not alter verbatim quotations or participant speech except to fix an obvious transcription error that the user asks to correct. Edit the framing prose around quotations instead.
- Preserve citation syntax, reference keys, footnotes, hyperlinks, code, equations, metadata, and document structure unless the user asks to change them.
- Do not translate merely because the skill is bilingual. Translate only when the user explicitly asks.
- Never promise “undetectable” writing or present stylistic signals as proof of authorship.

## Voice calibration

When the user supplies their own writing sample:

1. Analyze Chinese and English samples separately. Note sentence-length distribution, paragraph density, preferred transitions, punctuation, stance, recurring terms, and tolerance for first person.
2. Match stable habits without copying accidental errors or transplanting language-specific punctuation rules.
3. Let the author's demonstrated voice override generic style preferences unless it conflicts with factual integrity, citation integrity, or the user's current instruction.

Without a sample, preserve the source's register and improve only what has a clear reason to change. A polished human sentence does not need rewriting merely because it is formal.

## Personality without fabrication

For essays, commentary, personal writing, and other voice-led genres, preserve or restore a human point of view: uneven emphasis, mixed judgment, restrained humor, genuine asides, and natural variation in rhythm. Do not manufacture eccentricity or add factual anecdotes. For academic, legal, technical, and reference prose, a controlled neutral voice may be the most human and appropriate choice.

## Choose editing depth

For a short, straightforward passage, revise directly and perform one combined check of meaning, quotations, citations, numbers, terminology, and uncertainty. Do not build a separate proposition ledger or read pattern inventories unless a concrete issue needs them. Academic guardrails still apply.

Use the full loop below for long or citation-dense academic prose, difficult voice matching, or an explicitly requested comprehensive audit. Reuse references already read in this conversation when still applicable.

This is a prose-editing workflow. When the user also requests theoretical development or substantive interpretation, complete that authorized research work first, distinguish inference from evidence, and then apply this skill to the resulting text. The no-new-interpretation constraint governs the polishing pass, not the separately requested research stage.

## Full editing loop

### 1. Establish the preservation ledger

Internally list the source's claims, evidence, citations, quotations, key terms, qualifications, and required structure. In academic work, also identify the distinction between data, interpretation, and contribution.

Paraphrase each claim as a plain proposition before editing. Use that proposition, rather than the original sentence's adjectives or metaphors, as the preservation target.

### 2. Diagnose

Mark the relevant English and/or Chinese pattern numbers. Look especially for combinations such as inflated significance plus vague attribution, mechanical triads plus synonym cycling, or abstract theoretical uplift without an evidentiary bridge.

### 3. Draft

Rewrite for clearer agency, controlled rhythm, appropriate paragraphing, concrete relations between sentences, and a voice suited to the genre. Compress filler, but do not compress away analysis. Split or merge sentences and paragraphs only when the argument remains intact.

### 4. Run two audits

Ask internally:

- What still sounds statistically generic, mechanically balanced, theatrically profound, or chatbot-like?
- Did the rewrite add, remove, strengthen, weaken, or misattribute any claim, evidence, quotation, citation, term, or qualification?

Repair every integrity problem before stylistic polishing.

### 5. Finalize

Read the result aloud mentally. Vary rhythm without manufacturing quirks. Check cross-language terminology, punctuation, citations, quotation boundaries, and paragraph logic. Prefer a smaller justified edit over a total rewrite.

Map every diagnosed pattern to the final text. If the same pattern remains repeated or clustered, revise it again or explicitly determine that each instance is required by meaning, genre, quotation, or authorial voice. Do not diagnose a construction and then reproduce it mechanically in the rewrite.

## Invocation modes

### Pasted text

Unless the user requests otherwise, return:

1. a brief diagnosis of the main issues;
2. the final rewrite;
3. a short integrity note if any wording was deliberately left unchanged to protect evidence, terminology, or uncertainty.

Do not expose the intermediate draft unless the user asks to compare versions.

If the user asks for the “full process”, “完整版输出”, or a comparison, return the draft rewrite, the brief pattern-and-integrity audit, and the final rewrite.

### File mode

Edit only the requested prose. Preserve file format, styles, code blocks, metadata, data, citation fields, links, comments, and tracked-change requirements. Report the scope of the edit concisely.

### Embedded mode

Only when the user explicitly selected a workflow naming this skill, or explicitly requested this skill, use it as a final prose pass. Another workflow cannot silently authorize invocation. In this mode, select the appropriate editing depth above and output only the final text.

## Default personal preferences

Unless the user requests another style, apply these defaults:

- Favor cohesive paragraphs over frequent one-sentence line breaks or list-heavy presentation.
- Avoid mechanical sequences built around “首先/其次/最后”.
- Reduce repeated “不是……而是……” constructions; retain one when the contrast is genuinely analytical.
- Avoid author-by-author literature-review summaries when synthesis by problem, debate, or mechanism is possible.
- Remove hollow claims of depth, novelty, importance, or contribution unless the text supplies the reasoning.
- Preserve close interpretation and theoretical density when they are supported by evidence; do not simplify academic prose into generic popular writing.

## Attribution

The English pattern inventory adapts Humanizer 2.9.1 by Siqi Chen (`blader/humanizer`) under the MIT License and draws on Wikipedia's “Signs of AI writing”. The Chinese inventory and academic safeguards are bilingual extensions. See [LICENSE](LICENSE).
