# Pipeline Context

## Phase 1: 事实提取 — Entry Point of the Deconstruction Pipeline

`pop-decon-extract` is the **entry point** of the bottom-up deconstruction pipeline. It is the inverse of the creative writing process: while writing goes from story engine → world → plot → prose, deconstruction starts by extracting facts from the prose.

### Consumes

- **Novel TXT file** — raw text of the novel (typically downloaded via `tool-download-webnovel`).
- **`extract.py`** — ETL script that parses the TXT into structured JSON data.

### Produces

1. **`_temp/baseline-data.json`**, **`chapter-index.json`**, **`world-data.json`** — structured data extracted from the raw TXT.
2. **Character cards** (`状态/角色/`) — Lv4 protagonist card, Lv3 supporting character cards, walk-on pool.
3. **Fact skeleton** (`写作资产/事实骨架/`) — per-chapter event chains (Lv2/Lv3 only).
4. **Phase 1 summary** (`_参考书/{书名}/Phase1-事实提取摘要.md`).

### Downstream Consumers

| Phase | Skill | What It Consumes |
|:------|:------|:-----------------|
| Phase 2 | `pop-decon-cluster` (planned) | `_temp/` JSON files, fact skeleton, character cards → cluster volumes/acts |
| Phase 3 | `pop-decon-induce-world` (planned) | `_temp/world-data.json`, character cards, volume/act boundaries → L1 world-building |
| Phase 4 | `pop-decon-induce-engine` (planned) | Full Phase 1-3 outputs → story engine |

### Quality Gates

- **ETL must execute first** — no Phase 1 output may be written before `extract.py` has run.
- **Every fact must cite `chXX` evidence** — no unsourced data is allowed.
- **Inference must be marked** — any data derived from indirect evidence must be tagged `「推断」`.
- **No story engine in Phase 1** — Phase 1 extracts facts only; story engine induction belongs to Phase 4 (Lv3 only).
