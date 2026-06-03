"""
ESM / updater.py — 实体状态更新器（v2.0 · SQLite 支持）

职责：
  从事实骨架中提取实体的状态变化，写入 SQLite 或 YAML。
  双模式：
    - SQLite 模式（db_path 提供时写入 state_changelog 等表）
    - YAML 降级（db_path 为空时写回 YAML 文件）

使用：
  updater = EntityUpdater("/path/to/project", db_path=".../v3.db")
  changes = updater.detect_changes(fact_skeleton_text)
  updater.apply_changes(changes, chapter=201)
"""

import os
import re
import json
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
from loader import EntityLoader


class EntityUpdater:
    """实体状态更新器 —— 双模式（SQLite / YAML）"""

    CHANGE_PATTERN = re.compile(
        r'\{([^}]+)\}\s*\.\s*([a-zA-Z_\u4e00-\u9fff]+)\s*:\s*(.+?)$',
        re.MULTILINE
    )

    def __init__(self, project_root: str, db_path: Optional[str] = None):
        self.project_root = project_root
        self.db_path = db_path
        self.loader = EntityLoader(project_root, db_path=db_path)
        self._db_conn: Optional[sqlite3.Connection] = None

    def _get_db(self) -> sqlite3.Connection:
        if self._db_conn is None and self.db_path:
            self._db_conn = sqlite3.connect(self.db_path)
            self._db_conn.execute("PRAGMA foreign_keys = ON")
        return self._db_conn

    def close(self):
        if self._db_conn:
            self._db_conn.commit()
            self._db_conn.close()
            self._db_conn = None
        self.loader.close()

    # ─── 公共 API ─────────────────────────────────

    def detect_changes(self, skeleton: str) -> List[dict]:
        """
        从事实骨架文本中检测实体状态变化。
        匹配格式: {苏午}.心态: 冷静
        """
        changes = []
        for match in self.CHANGE_PATTERN.finditer(skeleton):
            entity_name = match.group(1).strip()
            field = match.group(2).strip()
            new_value = match.group(3).strip()
            changes.append({
                "entity": entity_name,
                "field": field,
                "new_value": new_value,
            })
        return changes

    def detect_entities_from_skeleton(self, skeleton_text: str, chapter: int) -> List[dict]:
        """
        Phase 2 修复: 从 {实体名} 标记中提取实体及其隐含的状态变化。
        替代原有只依赖 {实体}[:].字段: 值的格式，覆盖骨架中的纯标记。

        示例: {林深}在{客厅}打开了{诡异APP}
           → 林深: last_appearance=chapter
           → 客厅: last_appearance=chapter  
           → 诡异APP: last_appearance=chapter
        """
        refs = EntityLoader.extract_entity_references(skeleton_text)
        if not refs:
            return []

        # 过滤掉明显不是实体的通用描述词
        NON_ENTITY_WORDS = {
            '黑色', '白色', '灰色', '红色', '光', '黑', '字', '词', '名称',
            '文字', '样式', '颜色', '声音', '画面', '图片', '照片', '相册',
            '屏幕', '界面', '图标', '按钮', '链接', '动画', '音效', 'UI',
            '字体', '等宽字体', '提示', '翻译', '来源', '调试', '原始信息',
            '详情', '详细说明', '即时消息', '痕迹', '底层', '实体名', '来源分析',
            '手指', '大脑', '组合', '手指', '截屏',
            '数据删除', '残留', '普通残留', '高品质残留', '资源',
            '信息', '格式', '方向', '位置', '目标', '方式', '模式',
            '客厅', '楼道', '房间', '小区', '停车场', '区域', '门',
            '卧室', '阳台', '走廊', '窗户', '街道', '路灯', '墙壁',
        }

        changes = []
        for name in refs:
            if not name or len(name) < 1:
                continue
            if name in NON_ENTITY_WORDS:
                continue

            # 每个实体至少记录 "出现在了这章"
            changes.append({
                "entity": name,
                "field": "last_appearance",
                "new_value": str(chapter),
            })

            # 尝试从骨架上下文中推断位置变化
            loc_pattern = re.compile(
                r'\{' + re.escape(name) + r'\}(?:在|来到|走到|站在|进入|回到)(\{([^}]+)\})?'
            )
            m = loc_pattern.search(skeleton_text)
            if m and m.group(2):
                changes.append({
                    "entity": name,
                    "field": "位置",
                    "new_value": m.group(2),
                })

        # 去重
        seen = set()
        unique = []
        for c in changes:
            key = (c["entity"], c["field"])
            if key not in seen:
                seen.add(key)
                unique.append(c)
        return unique

    def apply_changes(self, changes: List[dict], chapter: int) -> int:
        """将变化清单持久化"""
        if self.db_path:
            return self._apply_to_db(changes, chapter)
        return self._apply_to_yaml(changes, chapter)

    def apply_changes_from_skeleton(self, skeleton_file: str, chapter: int) -> int:
        """从事实骨架文件读取并应用状态变化（Phase 2: 双格式检测）"""
        with open(skeleton_file, "r", encoding="utf-8") as f:
            skeleton = f.read()
        
        # 格式1: {实体}.字段: 新值（精确变化）
        changes = self.detect_changes(skeleton)
        
        # 格式2: {实体} 标记 → 推断状态变化（Phase 2新增回退）
        if not changes:
            changes = self.detect_entities_from_skeleton(skeleton, chapter)
        
        if not changes:
            print(f"[ESM] ⚠️ 事实骨架中未检测到状态变化: {skeleton_file}")
            return 0
        
        count = self.apply_changes(changes, chapter)
        print(f"[ESM] ✅ 实体状态更新完成: {count} 个变更 (db={'是' if self.db_path else '否'})")
        return count

    # ─── SQLite 写入 ──────────────────────────────

    def _apply_to_db(self, changes: List[dict], chapter: int) -> int:
        """写入 SQLite state_changelog"""
        conn = self._get_db()
        if not conn:
            return 0
        cur = conn.cursor()

        cur.execute("SELECT id FROM books WHERE id=1")
        row = cur.fetchone()
        book_id = row[0] if row else 1

        # 加载最近5章 changelog 用于去重
        recent_changes = set()
        try:
            cur.execute("""
                SELECT entity_id, field_changed, new_value FROM state_changelog
                WHERE chapter_id IN (SELECT DISTINCT chapter_id FROM state_changelog ORDER BY chapter_id DESC LIMIT 5)
            """)
            for r in cur.fetchall():
                recent_changes.add((r[0], r[1], r[2]))
        except:
            pass

        updated = 0
        for c in changes:
            entity_name = c["entity"]
            field = c["field"]
            new_value = c["new_value"]

            # 找实体在各表中的ID
            entity_id, entity_type = self._resolve_entity(cur, book_id, entity_name)
            if not entity_id:
                # 找不到实体：可能是新的，自动创建占位角色
                print(f"[ESM] ⚠️ 更新未找到实体，将自动创建: {entity_name}")
                entity_id = self._auto_create_entity(cur, book_id, entity_name)
                if not entity_id:
                    continue
                entity_type = 'character'

            # 跨章去重检查：同实体的同字段在最近5章是否已有相同值
            if (entity_id, field, new_value[:200]) in recent_changes:
                continue

            # 特殊字段处理：直接更新对应表的字段
            field_map = {
                "位置": "last_appearance",
                "location": "last_appearance",
                "心态": "brief",
                "current_mindset": "brief",
                "目标": "notes",
                "current_goal": "notes",
                "状态": "status",
                "health": "status",
            }

            db_field = field_map.get(field)
            if db_field:
                tbl = self._type_to_table(entity_type)
                if tbl:
                    try:
                        cur.execute(f"UPDATE {tbl} SET {db_field}=? WHERE id=?", (new_value[:200], entity_id))
                    except sqlite3.OperationalError:
                        pass

            # 总是写入 state_changelog
            cur.execute("""
                INSERT INTO state_changelog 
                (book_id, entity_type, entity_id, chapter_id, field_changed, old_value, new_value, change_reason)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (book_id, entity_type, entity_id, chapter, field, 
                  self._get_old_value(cur, entity_type, entity_id, field),
                  new_value[:200], 
                  f"[ESM] auto from ch{chapter}"))

            updated += 1

        # last_appearance 同步：所有涉及实体更新最后出现章
        for c in changes:
            entity_name = c["entity"]
            entity_id, entity_type = self._resolve_entity(cur, book_id, entity_name)
            if entity_id:
                tbl = self._type_to_table(entity_type)
                if tbl:
                    try:
                        cur.execute(f"UPDATE {tbl} SET last_appearance=? WHERE id=?", (chapter, entity_id))
                    except sqlite3.OperationalError:
                        pass

        conn.commit()
        print(f"[ESM] ✅ SQLite 已更新: {updated} 项变更")
        return updated

    def _resolve_entity(self, cur, book_id: int, name: str) -> tuple:
        """解析实体名 -> (entity_id, entity_type)"""
        tables = [
            ('characters', 'character'),
            ('weirds', 'weird'),
            ('skills', 'skill'),
            ('items', 'item'),
        ]
        for tbl, etype in tables:
            cur.execute(f"SELECT id FROM {tbl} WHERE name=? AND book_id=?", (name, book_id))
            row = cur.fetchone()
            if row:
                return row[0], etype
        return None, None

    def _auto_create_entity(self, cur, book_id: int, name: str) -> Optional[int]:
        """Phase 2: 自动创建占位实体——智能识别实体类型"""
        try:
            tbl = 'characters'
            
            # 玩家编号模式: 001-006 或 玩家001
            if re.match(r'^(玩家)?\d{3}$', name) or re.match(r'^00[1-9]$', name):
                tbl = 'characters'
            # 系统/道具类
            elif name in ['诡异APP', '诡异残留', '系统', '钥匙', '结晶钥匙']:
                tbl = 'items'
            # 诡异/怪物类
            elif any(k in name for k in ['诡异', '诡', '影', '路灯', '隙', '镜']):
                tbl = 'weirds'
            # 技能类
            elif any(k in name for k in ['Lv', '等级', '技能', '天赋', '探测']):
                tbl = 'skills'
            # 地点类
            elif any(k in name for k in ['客厅', '楼道', '房间', '小区', '停车场', '区域']):
                tbl = 'characters'  # locations aren't a separate table yet, treat as character
            
            try:
                cur.execute(f"SELECT 1 FROM {tbl} LIMIT 1")
            except sqlite3.OperationalError:
                tbl = 'characters'  # fallback
            
            if tbl == 'items':
                cur.execute("""
                    INSERT OR IGNORE INTO items
                    (book_id, name, type, description, first_appearance, notes)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (book_id, name, 'misc', f"[auto] 自动创建", None, 'auto-created'))
            elif tbl == 'weirds':
                cur.execute("""
                    INSERT OR IGNORE INTO weirds
                    (book_id, name, brief, first_appearance, notes)
                    VALUES (?, ?, ?, ?, ?)
                """, (book_id, name, f"[auto] 自动创建", None, 'auto-created'))
            elif tbl == 'skills':
                cur.execute("""
                    INSERT OR IGNORE INTO skills
                    (book_id, name, type, description, first_appearance, notes)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (book_id, name, 'system', f"[auto] 自动创建", None, 'auto-created'))
            else:
                cur.execute("""
                    INSERT OR IGNORE INTO characters 
                    (book_id, name, brief, importance, first_appearance, last_appearance, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (book_id, name, f"[auto] 从骨架自动创建", 3, None, None, 'auto-created'))
            
            cur.execute(f"SELECT id FROM {tbl} WHERE name=? AND book_id=?", (name, book_id))
            row = cur.fetchone()
            return row[0] if row else None
        except Exception as e:
            print(f"[ESM] ⚠️ 自动创建实体失败 ({name}): {e}")
            return None

    def _get_old_value(self, cur, entity_type: str, entity_id: int, field: str) -> str:
        """获取字段旧值"""
        tbl = self._type_to_table(entity_type)
        if not tbl:
            return ""
        field_map = {
            "位置": "last_appearance", "location": "last_appearance",
            "心态": "brief", "current_mindset": "brief",
            "状态": "status", "health": "status",
        }
        col = field_map.get(field, "brief")
        try:
            cur.execute(f"SELECT {col} FROM {tbl} WHERE id=?", (entity_id,))
            row = cur.fetchone()
            return str(row[0]) if row else ""
        except:
            return ""

    def _type_to_table(self, entity_type: str) -> Optional[str]:
        mapping = {
            'character': 'characters', 'weird': 'weirds',
            'skill': 'skills', 'item': 'items',
        }
        return mapping.get(entity_type)

    # ─── YAML 写入（原逻辑）───────────────────────

    def _apply_to_yaml(self, changes: List[dict], chapter: int) -> int:
        """写回 YAML 实体卡（原 updater 逻辑）"""
        import yaml

        grouped: Dict[str, List[dict]] = {}
        for c in changes:
            name = c["entity"]
            if name not in grouped:
                grouped[name] = []
            grouped[name].append(c)

        updated_count = 0
        for entity_name, entity_changes in grouped.items():
            ok = self._update_single_yaml(entity_name, entity_changes, chapter)
            if ok:
                updated_count += 1
        return updated_count

    def _update_single_yaml(self, entity_name: str, changes: List[dict], chapter: int) -> bool:
        """更新单个实体的 YAML 文件"""
        import yaml
        card_path = self.loader.find_card(entity_name)
        if card_path is None:
            print(f"[ESM] ⚠️ 跳过未找到的实体: {entity_name}")
            return False

        with open(card_path, "r", encoding="utf-8") as f:
            card = yaml.safe_load(f)
        if card is None:
            card = {}
        if "state" not in card:
            card["state"] = {}

        state = card["state"]
        for c in changes:
            field = c["field"]
            new_value = c["new_value"]

            if field in ("位置", "location"):
                state["location"] = new_value
            elif field in ("心态", "current_mindset"):
                state["current_mindset"] = new_value
            elif field in ("目标", "current_goal"):
                state["current_goal"] = new_value
            elif field == "状态":
                if "health" not in state:
                    state["health"] = {}
                state["health"]["status"] = new_value
            elif field in ("纹路数", "hp", "经验值"):
                state[field] = new_value
            elif field == "已掌握":
                if "skills" not in state:
                    state["skills"] = {}
                state["skills"]["mastered"] = [s.strip() for s in new_value.split(",")]
            elif "." in field:
                parts = field.split(".")
                target = state
                for part in parts[:-1]:
                    if part not in target:
                        target[part] = {}
                    target = target[part]
                target[parts[-1]] = new_value
            else:
                state[field] = new_value

        history_entry = {
            "chapter": chapter,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "changes": [{"field": c["field"], "new_value": c["new_value"]} for c in changes],
        }
        if "state_history" not in state:
            state["state_history"] = []
        state["state_history"].append(history_entry)

        with open(card_path, "w", encoding="utf-8") as f:
            yaml.dump(card, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        print(f"[ESM] ✅ 已更新 YAML: {entity_name} ({len(changes)} 项变化)")
        return True
