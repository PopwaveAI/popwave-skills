# DeepSeek Executor Runbook

## Goal

Use this runbook when a lower-cost agent needs to execute a title-to-TXT webnovel download with minimal judgment. The target output is a verified TXT plus a quality report. If a complete TXT cannot be verified, return a clean partial only after documenting rejected complete-source attempts.

## Input Contract

Required:

- Book title.

Optional but strongly preferred:

- Author.
- Original platform.
- Expected chapter or section count.
- Completion scope: completed full book, current published chapters, or a user-specified range.
- Authorized source URL, cookie file, browser export, local archive, or local HTML export.
- Target-specific terms for drift detection, such as protagonist names, place names, sect names, or unique concepts.

## Output Contract

Return these fields at the end of every run:

- `status`: `PASS`, `PARTIAL`, or `FAIL`.
- `txt_path`: final TXT path, or empty if failed.
- `quality_report`: JSON report path, or empty if unavailable.
- `completion_status`: value from the quality report.
- `acceptance_status`: value from the quality report.
- `scope`: completed full book, current published chapters, user range, or largest clean partial.
- `expected_sections`: trusted expected count, URL count, archive section count, or unknown.
- `source_used`: final accepted source.
- `sources_rejected`: list of rejected sources and exact reasons.
- `commands_run`: enough command lines to reproduce the final result.
- `notes`: only material caveats, such as source-intrinsic corrupt lines or partial fallback reason.

## Deterministic Workflow

1. Define scope and expected count.
   - If the user gives an official platform or ranking basis, use it to identify the book and expected chapter count.
   - If the work is ongoing, call the scope "current published chapters", not "completed full book".
   - If the expected count is unknown, continue, but final acceptance must rely more heavily on source samples and suspicious-count checks.
   - If search corrects an obvious typo, record both the user query and the accepted canonical title.

2. Try title-only automation first.

```bash
python3 scripts/download_novel.py \
  --auto-title "BOOK_TITLE" \
  --output work/BOOK_SLUG.txt \
  --candidates-output work/BOOK_SLUG.candidates.json \
  --quality-output work/BOOK_SLUG.quality.json \
  --urls-output work/BOOK_SLUG.urls.txt \
  --auto-try-candidates 5 \
  --delay 0.5 \
  --delay-jitter 0.2 \
  --retries 2 \
  --timeout 30
```

3. If title-only output exists, validate it again with the strongest known checks.

```bash
python3 scripts/download_novel.py \
  --quality-report work/BOOK_SLUG.txt \
  --expected-sections EXPECTED_COUNT \
  --expected-numeric-sections EXPECTED_COUNT \
  --require-chapter-number-sequence \
  --required-term "TERM_A|TERM_B|TERM_C" \
  --output work/BOOK_SLUG.final-quality.json
```

Use `--expected-numeric-sections` and `--require-chapter-number-sequence` only when the book has one continuous numeric chapter sequence. Skip numeric continuity for multi-volume works where chapter numbers reset.

4. Accept only if the quality report passes.
   - `acceptance_status: pass` is required for complete success.
   - Suspicious counts must be zero or manually explained after sample inspection.
   - `html_markup_noise`, access-gate text, duplicate section fingerprints, missing numeric sequence, or required-term misses reject the source.
   - If title-only automation downloads a short metadata/intro TXT with zero detected sections, reject it and continue to the next candidate.
   - Use `--required-term` only when source drift is plausible. Side-story番外 can legitimately omit the main cast.

5. If the first source fails, classify candidates and probe alternatives.

```bash
python3 scripts/download_novel.py \
  --discover-title "BOOK_TITLE" \
  --output work/BOOK_SLUG.discover.json \
  --discover-max 10
```

For each promising candidate:

```bash
python3 scripts/download_novel.py \
  --probe-url "SOURCE_URL" \
  --output work/BOOK_SLUG.probe-N.json
```

Prioritize real direct TXT/ZIP/EPUB/RAR sources and complete TOC sources. Reject gate placeholders, JS challenges, app-only placeholders, and obviously unrelated candidates.

6. For direct file, archive, or download-detail pages, use the matching extraction path.

```bash
python3 scripts/download_novel.py \
  --download-file-from "SOURCE_URL" \
  --download-output work/BOOK_SLUG.raw.bin \
  --output work/BOOK_SLUG.from-download.txt \
  --title "BOOK_TITLE" \
  --input-encoding gb18030 \
  --drop-line "广告|下载|最新网址" \
  --dedupe-adjacent-lines
```

If a raw archive is already present:

```bash
python3 scripts/download_novel.py \
  --extract-zip work/BOOK_SLUG.zip \
  --output work/BOOK_SLUG.from-zip.txt \
  --title "BOOK_TITLE" \
  --input-encoding gb18030
```

```bash
python3 scripts/download_novel.py \
  --extract-epub work/BOOK_SLUG.epub \
  --output work/BOOK_SLUG.from-epub.txt \
  --title "BOOK_TITLE" \
  --dedupe-adjacent-lines \
  --min-section-chars 80
```

7. For TOC sources, extract links and boundary-test before a full run.

```bash
python3 scripts/download_novel.py \
  --extract-chapter-links-auto-from "TOC_URL" \
  --output work/BOOK_SLUG.urls.txt
```

If the TOC was saved locally with curl, preserve relative URL resolution:

```bash
python3 scripts/download_novel.py \
  --extract-chapter-links-auto-from work/BOOK_SLUG.toc.html \
  --base-url "ORIGINAL_TOC_URL" \
  --output work/BOOK_SLUG.urls.txt
```

Boundary-test first, middle, and last URLs, plus any known weak positions around public/VIP boundaries.

```bash
python3 scripts/download_novel.py \
  --urls-file work/BOOK_SLUG.boundary-urls.txt \
  --output work/BOOK_SLUG.boundary.txt \
  --title "BOOK_TITLE" \
  --content-selector "#content" \
  --title-selector "h1" \
  --page-link-regex "_[0-9]+\\.html" \
  --page-link-sort-numeric "_([0-9]+)\\.html" \
  --failure-output work/BOOK_SLUG.boundary.failed.txt \
  --delay 0.5 \
  --delay-jitter 0.2 \
  --retries 3
```

Only run the full TOC after boundary samples contain real target prose.

```bash
python3 scripts/download_novel.py \
  --urls-file work/BOOK_SLUG.urls.txt \
  --output work/BOOK_SLUG.full.txt \
  --title "BOOK_TITLE" \
  --content-selector "#content" \
  --title-selector "h1" \
  --page-link-regex "_[0-9]+\\.html" \
  --page-link-sort-numeric "_([0-9]+)\\.html" \
  --failure-output work/BOOK_SLUG.full.failed.txt \
  --flush-each \
  --delay 0.5 \
  --delay-jitter 0.3 \
  --retries 3 \
  --timeout 35
```

8. For official or authorized JJWXC pages, use the JJWXC mode.

```bash
python3 scripts/download_novel.py \
  --urls-file work/BOOK_SLUG.jjwxc-urls.txt \
  --output work/BOOK_SLUG.official.txt \
  --title "BOOK_TITLE" \
  --content-mode jjwxc \
  --cookie-file work/authorized-cookie.txt \
  --delay 0.8 \
  --retries 3
```

Use only the user's authorized session, supplied export, or public official chapters. Do not attempt captcha solving, token guessing, credential stuffing, DRM removal, or other access-control circumvention.

9. Partial fallback is the last step.
   - It is allowed only after complete-source attempts are logged and rejected.
   - Use the largest verified clean chapter set, not the largest polluted file.
   - Mark it as partial in filename, quality report, and final status.

```bash
python3 scripts/download_novel.py \
  --quality-report work/BOOK_SLUG.public-partial.txt \
  --expected-sections EXPECTED_COUNT \
  --allow-partial-quality \
  --partial-reason "Full sources rejected: SOURCE_A reason; SOURCE_B reason. This is the largest verified clean chapter set." \
  --output work/BOOK_SLUG.public-partial.quality.json
```

## Acceptance Rules

Return `PASS` only when:

- The TXT covers the defined scope.
- `acceptance_status` is `pass`.
- First, middle, and last samples are real target prose.
- No failed URLs remain for required chapters.
- Duplicate fingerprint, gate, HTML, mojibake, and drift checks are clean or explicitly benign.

Return `PARTIAL` only when:

- Complete-source attempts were rejected with reasons.
- The delivered TXT is the largest verified clean set.
- The quality report says `acceptance_status: partial`.
- The only blocking issue is missing sections versus the expected complete count.

Return `FAIL` when:

- No clean complete or partial TXT can be verified.
- Available files contain HTML, gate placeholders, source drift, duplicate fake chapters, corrupted text, or unresolved missing chapters.

## Execution Notes

- Do not rename an unverified TXT to `final`.
- Do not call a file successful because it is large.
- Do not treat HTTP 200 as proof of chapter availability.
- Do not stop title-only runs on the first physical TXT file if its quality report fails.
- Do not reject an old multi-volume novel only because chapter titles repeat. Reject duplicate正文 fingerprints or missing URL/block coverage instead.
- Prefer reproducible command logs over narrative.
- Keep all intermediate candidates and failed-source notes; they are useful regression cases.
