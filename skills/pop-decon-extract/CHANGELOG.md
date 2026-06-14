# CHANGELOG

## v1.0.0 (2026-06-14)

### Added
- Initial release of `pop-decon-extract` skill.
- Extracted from `pop-decon` v12 Phase 1 as an independent skill.
- Core ETL pipeline: `extract.py all {txt_path} {output_dir}` → `_temp/` three JSON files.
- Character card extraction: Lv4 (protagonist) + Lv3 (supporting) + walk-on pool.
- Fact skeleton extraction (Lv2/Lv3): per-chapter event chain.
- Phase 1 summary report generation.
- Quality red lines imported from `pop-decon` v12.
- Templates: `character-lv3.tpl.md`, `character-lv4.tpl.md`.
