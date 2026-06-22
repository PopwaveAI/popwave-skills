# CHANGELOG

## v3.0.1 (2026-06-22)

- Re-emphasized direct-link download as the primary workflow.
- Clarified that acceptable sources are authorized TXT/ZIP direct links or local files.
- Preserved boundaries against prioritizing infringing repost sites, bypassing access controls, and protected-site chapter crawling.

## v3.0.0 (2026-06-22)

- Reframed skill from "search direct links" to authorized source download/import.
- Added `scripts/download_text.py` for URL/local file import, ZIP extraction, UTF-8 normalization, HTML/error-page detection, and size validation.
- Replaced `steps/step-1-search.md` with `steps/step-1-source.md` to enforce source/permission checks.
- Updated SKILL.md and skill.json to forbid piracy-oriented search, login/paywall bypass, protected-site crawling, and full-text pasteback.

## v2.0.1 (2026-06-14)

- v5 structural refactoring: added CHANGELOG.md, steps/ directory with step-1-search.md / step-2-download.md / step-3-verify.md, drop-point check table, steps references in SKILL.md, pipeline field in skill.json.

## v2.0.0 (2026-06-13)

- Initial release. SOP with lookup table, red lines, WRONG examples, error handling.
