# Failure Decision Table

Use this table to classify outputs before accepting a TXT.

| Signal | Detection | Status | Next Action |
|---|---|---|---|
| HTML saved as TXT | `html_markup_noise > 0`, or visible `<!DOCTYPE`, `<html>`, `<body>`, `<script>`, layout tags | FAIL | Reject the source or follow the real download link. Do not clean HTML into a final TXT. |
| Intro or metadata TXT | Very short TXT, no detected sections, samples are简介/主播/metadata rather than chapters | FAIL | Reject the candidate and continue title-only search. |
| Access gate or placeholder | Quality report gate counts, or text like password prompt, captcha, app-only, login required, copyright placeholder | FAIL | Use authorized session/export if available; otherwise reject the source. |
| JS or Cloudflare challenge | Page asks to enable JavaScript/cookies, challenge page, empty scripted shell | FAIL | Use browser/export only if user-authorized; otherwise switch source. |
| Duplicate chapter bodies | `unique_block_section_count < block_section_count`, duplicate fingerprints | FAIL | Reject generated URL template or mirror; find real TOC/source. |
| Duplicate chapter titles only | Repeated titles such as `第一章` across volumes, but unique fingerprints are clean | PASS CANDIDATE | Validate block count, unique fingerprints, and samples. Do not require numeric continuity. |
| Missing numeric sequence | `missing_numeric_chapter_numbers_count > 0` with `--require-chapter-number-sequence` | FAIL | Try backup source or archive. Skip this check only for multi-volume numbering resets. |
| Required-term misses | `required_term_missing_section_count > 0` | FAIL | Treat as source drift or unrelated book text; reject source unless manual inspection proves terms were wrong. |
| Required-term misses only in side番外 | Misses occur in inspected番外 focused on other characters | MANUAL REVIEW | Rerun quality without required-term or with broader terms after confirming samples are still target text. |
| VIP/public boundary drift | First public chapters are correct, later mirror chapters switch style/names/book | FAIL | Use official authorized session/export or mark official public portion as partial fallback. |
| Font obfuscation/private-use | High private-use count, unreadable glyphs, fake font substitution | FAIL | Use official/export path or another source. Do not deliver unreadable text. |
| Mojibake after decode | Replacement characters, broken Chinese, wrong encoding | RETRY | Normalize with smart decode, `gb18030`, `gbk`, or alternate archive member. Fail only if source-intrinsic damage remains unresolved. |
| Source boilerplate at file edges | Source credits, upload wrappers, repeated decorative separators | RETRY | Normalize/clean using narrow `--drop-line` or default boilerplate cleanup, then rerun quality. |
| Inline tail marker | Final prose line ends with a narrow marker such as `gd1806102:` | RETRY | Strip the marker only; preserve the story line. |
| Navigation or ads inside正文 | Repeated next/previous/menu/download lines in samples | RETRY | Tighten `--content-selector`, `--start-after`, `--end-before`, `--drop-line`, or switch source. |
| In-chapter pagination missing | Chapter page has page controls and truncated body | RETRY | Add `--page-link-regex` and `--page-link-sort-numeric`; boundary-test again. |
| Rate-limit/timeouts | Many adjacent connection resets/timeouts, incomplete failed URL list | RETRY | Rerun with `--delay 0.5`, jitter, more retries, `--flush-each`, and resume where possible. |
| Slow archive server | Partial ZIP/RAR/EPUB response, supports `206` resume | RETRY/INCONCLUSIVE | Resume with curl or rerun later. Do not mark parser failure. |
| Sandbox DNS/network failure | Python fetch cannot resolve host, curl or escalated run works | RETRY | Rerun exact approved script command with network escalation, or save source with curl and parse local file with `--base-url`. |
| TOC count lower than expected | Clean source has fewer URLs than trusted official count | PARTIAL CANDIDATE | Keep only as fallback after complete attempts fail; label partial. |
| Official public only | Public chapters extract cleanly, VIP chapters require authorized session | PARTIAL CANDIDATE | Use public set only as fallback unless user supplies authorized cookie/export. |
| Unknown expected count | No trusted source exposes count | MANUAL REVIEW | Validate suspicious counts, first/middle/last samples, and source credibility. Avoid claiming completed full book. |
| Multi-volume numeric reset | Chapter numbers repeat by volume but block count matches URL/source count | PASS CANDIDATE | Do not use numeric continuity. Validate URL count, unique fingerprints, and samples. |
| Typo title corrected by source | User query and accepted source title differ by a plausible typo | PASS CANDIDATE | Record both titles and use accepted canonical title in the final TXT. |
| Benign keyword hit | Quality keyword occurs as real story/author text, not site noise | PASS CANDIDATE | Document briefly; do not delete story text. |

## Stop Conditions

Stop and return `PASS` when one source or merged output satisfies the defined scope and quality acceptance.

Stop and return `PARTIAL` when complete attempts are exhausted or gated, and the largest clean fallback has `acceptance_status: partial`.

Stop and return `FAIL` when all available candidates are gated, polluted, unrelated, unreadable, or unverifiable.
