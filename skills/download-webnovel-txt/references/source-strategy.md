# Source Strategy

## Source Priority

Prefer sources in this order:

1. Official platform export/download feature.
2. User-provided source pages or chapter lists.
3. User-provided local HTML/PDF/TXT exports.
4. Official chapter pages, partner sites, internal sources, or licensed mirrors.

Do not spend the interaction interrogating the user's rights. Assume the user has appropriate access unless the request explicitly asks for credentials, DRM cracking, captcha bypass, or similar circumvention.

## Login and Session Handling

If a site requires login:

- Ask the user to authenticate in a browser, then use browser extraction, exported HTML, or a user-provided cookie/session.
- Do not attempt credential stuffing, captcha solving, token guessing, DRM removal, or account takeover.
- If the platform has an official export/download feature, prefer that when it is practical.

## Chapter Discovery

Good chapter-list inputs include:

- A table of contents URL.
- A copied list of chapter URLs.
- A local HTML file containing chapter links.
- Search results from the official platform.
- A continuous URL template, such as `.../{n}.html`, when a site has chapter pages but no usable TOC.

For large novels, sample a few URLs first and confirm the pattern before collecting every chapter.
When the user provides only a title, start with `--discover-title`, then inspect/probe the top candidates. Treat `toc` candidates as chapter-page sources, `download-page-*` candidates as file-link sources, and `access-gated` candidates as source-selection failures.
If the input title contains a typo but search results consistently point to a clear canonical title, use the canonical title from the accepted source in the final TXT while preserving the user's original query in candidates and logs.
Ranking platforms can be used only as sample discovery sources. The final TXT source can be a different official page, user-authorized session, export/download file, or stable novel-site candidate, as long as the run is validated independently.
Define the completeness scope before acceptance: completed full book, current published chapters for an ongoing work, user-specified chapter range, or the chapter count exposed by a trusted TOC/export. Do not call an ongoing work a completed full-book download just because all current chapters were fetched.

## Quality Checks

Before delivering the TXT:

- Verify the first chapter starts with real prose, not menus.
- Verify a middle chapter is not a login/paywall placeholder.
- Verify the last chapter is present.
- Search for repeated boilerplate such as "next chapter", "previous chapter", "download app", and remove it only when doing so does not remove story text.
- Preserve chapter titles and order.
- Run `--quality-report --expected-sections N` when the URL list count or archive section count is known. A `complete` status with zero suspicious counts is the strongest local signal; still inspect the samples.
- Check unique section fingerprints, not only successful HTTP requests. Some sites return a valid page for every requested URL while silently repeating the last available chapter.

## Real Novel Site Pitfalls

- Do not assume chapter IDs are continuous. Prefer extracting chapter links from the real table-of-contents pages, then compare against the expected chapter count.
- If a source lacks a full TOC but has predictable numbered chapter URLs, generate a URL template list, then reject it if the quality report shows duplicate正文 fingerprints or fewer unique sections than expected.
- When a source has multiple TOC pages, pass every page to link extraction and sort/deduplicate by chapter ID or chapter number.
- Prefer the tightest正文容器 over full-page extraction. Examples: `#content`, `#chapterContentWapper`, `#chapter-content`.
- Check whether a single chapter is paginated. Pagination links like `chapter_2.html`, `chapter_3.html`, or visible `1 2 3 4` controls mean the first chapter URL is incomplete unless `--page-link-regex` is used.
- If a few pages fail under the tight selector, inspect one failed page with `--save-html`; the site may use a different template for removed/exception chapters.
- If many adjacent pages fail with connection reset or timeout but later pages work, the source is likely rate-sensitive. Rerun with `--delay 0.4` to `0.6`, `--delay-jitter 0.2` to `0.5`, `--retries 3`, and `--failure-output`; do not immediately switch sources.
- Use `--stop-after-consecutive-failures` when a source appears blocked, gated, or down, so a long run does not waste time producing hundreds of known failures.
- Keep a backup-source workflow: main source for most chapters, backup source for missing chapters, then merge by chapter number.
- For unstable TLS sites, Python `urllib` may time out while `curl -k --http1.1` succeeds. Fetch the HTML with curl, then pass local HTML files to the script.
- If curl can fetch a TOC but Python direct fetch disconnects, save the TOC locally and pass `--base-url` with the original page URL so relative chapter links resolve to real HTTP URLs.
- Download-detail pages may return an HTML gate instead of the archive/TXT. Phrases like "下载地址已被隐藏", "输入密码查看", "关注微信公众号", "由于版权问题不能显示", "APP内更新", password inputs, or captcha prompts mean the source is access-gated; do not waste retries. Use a user-provided password/export/file, or reject that source and continue with another one.
- Cloudflare challenge pages and "enable JavaScript/cookies" blocks are source-selection failures for this script. Do not treat them as empty chapters; move to another source or use the user's authenticated browser/export path.
- Always run final checks: chapter count, missing chapter numbers, first/last chapter, known boilerplate terms, and sampled补章 content.
- The default deliverable is a complete verified TXT. A partial TXT is allowed only as a named fallback after full-source attempts are documented and rejected. Use `--allow-partial-quality` with a `--partial-reason`, and label the file/report as partial instead of final.
- Partial fallback can pass only when the sole quality issue is fewer sections than the known expected count. Duplicate正文 fingerprints, target-term misses, source drift, gate placeholders, or corrupted text must remain `fail` even if they include more chapters.
- Direct TXT downloads may use GBK/GB18030 even when downloaded from modern pages. Inspect `file`/sample output; if text is mojibake, run `--normalize-txt --input-encoding gbk` or `gb18030` to produce UTF-8 output before cleanup.
- JJWXC official pages commonly use GB18030 markup plus compressed HTTP bodies, query-string chapter links, app-download links that look like dynamic downloads, and chapter titles without `第X章`. Use `--content-mode jjwxc` for authorized/public official chapter pages, validate by TXT block count, and keep app/client download links out of source classification.
- JJWXC VIP chapter rows may put the authorized reading URL in an anchor `rel` attribute such as `my.jjwxc.net/onebook_vip.php?...` rather than in `href`. Extract both public `onebook.php` links and VIP `onebook_vip.php` links to build the full chapter list, then require the user's authorized cookie/session for VIP正文 retrieval.
- Treat `--input-encoding` as a preference, not a guarantee. Some title-discovery sources expose UTF-8 TXT files even when similar sites usually use GB18030; smart decoding should be applied to normalization and cleanup paths too.
- After legacy-encoding conversion, scan for the replacement character `�` and Unicode private-use characters. If only a tiny number of lines remain corrupted, treat it as source-intrinsic text damage and either document it or patch from a backup source.
- EPUB is a ZIP container. Extract text by OPF spine order, not lexical filename order; files like `ch100.html` and skipped numeric IDs make naive sorting unreliable.
- EPUBs often include cover/short title pages, duplicated h1/body titles, and per-section publisher watermarks. Use `--min-section-chars`, `--dedupe-adjacent-lines`, `--drop-line`, and `--remove-regex` together, then rescan the final TXT.
- EPUBs can also include generated cover pages, global table-of-contents pages, and per-volume目录 pages in the spine. Skip these by default for a clean reading TXT; keep them only when the user asks for navigation pages.
- ZIP download pages may first return an HTML list page, not the archive itself. Inspect content type/file headers, extract the real archive URL from the list, then use resumable download for slow file servers.
- ZIP archives from Chinese novel sites often contain GBK/GB18030 TXT members. Use `--extract-zip --input-encoding gb18030`, and select a member with `--zip-member-regex` if the archive contains ads, readme files, or multiple editions.
- Some download buttons point to dynamic endpoints such as `/down/xs/?id=...` that return another HTML landing page. Use `--download-file-from`; it follows simple landing pages and sniffs the final file type from URL extension, content type, or magic bytes.
- If a dynamic download path saves HTML as `.txt`, reject it. Quality reports flag `html_markup_noise`; `<!DOCTYPE`, `<html>`, `<body>`, `<script>`, or closing layout tags inside a TXT are source failures, not cleanup chores.
- RAR/7z support depends on local archive tooling. Prefer `bsdtar` when present; otherwise classify the source as needing an external extractor rather than treating it as a download failure.
- Large direct downloads may time out near completion. Use a tool that supports resume, such as `curl -C -`, before classifying the source as failed.
- For multi-volume novels, chapter numbers often reset from "第一章" in each volume, or split into "(上)/(中)/(下)". Validate URL count versus output block count first. Numeric chapter-title checks are only auxiliary and `--merge-txt` by numeric chapter number can overwrite different volumes if used blindly.
- Repeated chapter titles in old multi-volume novels are not automatically duplicate content. Treat duplicate正文 fingerprints as failures; duplicate titles alone are only a review signal.
- For chapterized TXT output, numeric sequence validation should use section/block titles instead of every body line. Body text can contain old chapter titles, author notes, or embedded source artifacts that look like duplicate chapter numbers.
- Noise keyword scans can have false positives inside story text, especially words like "广告", "下载", or modern terms such as "微信" used literally. Inspect hits before deleting lines.
- Mirrors can silently replace unavailable VIP chapters with unrelated book text while still returning `200 OK`, unique URLs, and unique section blocks. Use `--required-term` with target-specific names/places and inspect first/middle/last samples before accepting a full TXT.
- Use `--required-term` selectively. It is best for suspected source drift after a known boundary, but it can overreject legitimate番外 or side-story chapters that do not mention the main cast.
- Common TXT wrappers can appear as source banners, upload disclaimers, or download-site credits at the start/end of a file. The script removes narrow known wrappers by default and trims decorative separator lines only at file edges; use `--keep-source-boilerplate` if a source intentionally needs those lines preserved.
- Title-only searches may surface a small introduction, metadata, or audio-book description TXT before the real full novel. Short TXT files with no detected sections should be rejected, and auto-title mode should continue to later candidates.
- Some direct TXT sources append narrow inline tail markers such as `gd1806102:` to the final prose line. Strip the marker without deleting the line.
- Quality heading detection should include Chinese enumerated headings such as `一、序章` as well as ordinary `第X章` headings. Also count short ending headings like `末章` and `后记`, but keep a length cap so afterword prose that begins with "后记..." is not misclassified as a new section. Short literary works may have no known expected section count, so use suspicious counts plus sample inspection as the acceptance signal.
- Avoid overbroad chapter-heading regexes. Prose lines like `第一回背出道德经的那天` or counting text like `一二三、四五六...` are not headings; require a separator after `第X章/回` and keep Chinese enumerated headings short.
