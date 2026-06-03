"""
ESM / validator.py — 实体状态一致性校验器（v2.0 · SQLite 支持）
"""
import os, re
from typing import List, Dict, Optional
from loader import EntityLoader


class EntityValidator:
    def __init__(self, project_root: str, db_path: Optional[str] = None):
        self.project_root = project_root
        self.db_path = db_path
        self.loader = EntityLoader(project_root, db_path=db_path)

    def check_consistency(self, chapter: int, skeleton_file: str) -> dict:
        items = []

        # ① 引用一致性
        ref_result = self._check_references(skeleton_file)
        items.append(ref_result)

        with open(skeleton_file, "r", encoding="utf-8") as f:
            skeleton = f.read()

        refs = EntityLoader.extract_entity_references(skeleton)

        # 对每个被引用的实体检查状态历史
        for entity_name in refs:
            card = self.loader.load_entity(entity_name)
            if card is None:
                continue

            state = card.get("state", {})
            history = state.get("state_history", [])
            hist_check = self._check_state_history(entity_name, history, chapter)
            items.append(hist_check)

            knowledge_check = self._check_knowledge(entity_name, card, chapter, skeleton)
            if knowledge_check:
                items.append(knowledge_check)

        failed = [i for i in items if i["status"] in ("❌", "⚠️")]
        report = {
            "pass": len(failed) == 0,
            "chapter": chapter,
            "total_checks": len(items),
            "passed": len(items) - len(failed),
            "failed": len(failed),
            "items": items,
            "summary": "✅ 全部通过" if len(failed) == 0 else f"⚠️ {len(failed)}/{len(items)} 项检查未通过",
        }
        return report

    def _check_references(self, skeleton_file: str) -> dict:
        with open(skeleton_file, "r", encoding="utf-8") as f:
            skeleton = f.read()
        refs = EntityLoader.extract_entity_references(skeleton)
        missing = []
        for name in refs:
            path = self.loader.find_card(name)
            if path is None:
                missing.append(name)
        if not missing:
            return {"check": "引用一致性", "status": "✅", "detail": f"所有 {len(refs)} 个引用均有对应实体"}
        return {"check": "引用一致性", "status": "❌", "detail": f"缺少 {len(missing)} 个实体: {', '.join(missing)}"}

    def _check_state_history(self, entity_name: str, history: List[dict], current_chapter: int) -> dict:
        if len(history) < 2:
            return {"check": f"{entity_name} 状态演变", "status": "✅", "detail": f"历史记录 {len(history)} 条"}
        chapters = sorted([h.get("chapter") for h in history if h.get("chapter")])
        gaps = []
        for i in range(len(chapters) - 1):
            diff = chapters[i+1] - chapters[i]
            if diff > 2:
                gaps.append(f"CH{chapters[i]} → CH{chapters[i+1]} (跳过 {diff-1} 章)")
        if not gaps:
            return {"check": f"{entity_name} 状态演变", "status": "✅", "detail": f"{len(history)} 条记录，章节连续"}
        return {"check": f"{entity_name} 状态演变", "status": "⚠️", "detail": f"状态跳变: {'; '.join(gaps)}"}

    def _check_knowledge(self, entity_name: str, card: dict, current_chapter: int, skeleton: str) -> Optional[dict]:
        state = card.get("state", {})
        revealed = state.get("knowledge", {}).get("revealed", [])
        if not revealed:
            return None
        unsupported = []
        for info in revealed:
            keywords = info[:8]
            if keywords not in skeleton:
                pass
        return None

    def check_reference_coverage(self) -> dict:
        all_entities = self.loader.list_all_entities()
        dead_refs = []
        for etype, names in all_entities.items():
            for name in names:
                card = self.loader.load_entity(name)
                if card is None:
                    continue
                state = card.get("state", {})
                rels = state.get("relationships", [])
                for rel in rels:
                    target = rel.get("target", "")
                    if not target:
                        continue
                    target_clean = target.strip("{}")
                    if self.loader.find_card(target_clean) is None:
                        dead_refs.append(f"{name} → {target}")
        return {
            "status": "✅" if not dead_refs else "⚠️",
            "total_entities": sum(len(v) for v in all_entities.values()),
            "dead_references": dead_refs,
            "detail": "所有关系引用均有效" if not dead_refs else f"存在 {len(dead_refs)} 个死引用:\n  " + "\n  ".join(dead_refs),
        }
