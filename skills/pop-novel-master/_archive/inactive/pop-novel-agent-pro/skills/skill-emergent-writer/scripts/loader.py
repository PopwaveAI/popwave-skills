"""
ESM / loader.py — 实体加载器（v2.0 · SQLite 优先）

职责：
  加载实体数据并拼成 context-bundle。
  双模式：
    - SQLite 优先（db_path 提供时从 v3.db 查询）
    - YAML 降级（db_path 为空时从 00-实体卡/ 读取 YAML）

使用：
  loader = EntityLoader("/path/to/project", db_path=".../v3.db")
  bundle = loader.build_context_bundle(["苏午", "尸陀鬼之手"])
"""

import os
import re
import json
import sqlite3
from typing import Dict, List, Optional, Tuple


class EntityLoader:
    """实体加载器 —— 双模式（SQLite 优先 / YAML 降级）"""

    TYPE_DIR_MAP = {
        "character": "character",
        "item": "item",
        "location": "location",
        "skill": "skill",
        "thread": "thread",
    }

    def __init__(self, project_root: str, db_path: Optional[str] = None):
        """
        初始化加载器。

        参数:
          project_root: 项目根目录（包含 00-实体卡/ 的路径）
          db_path: v3.db 文件路径。提供则走 SQLite 模式，否则走 YAML 降级。
        """
        self.project_root = project_root
        self.db_path = db_path
        self._db_conn: Optional[sqlite3.Connection] = None

        if not db_path:
            # YAML 模式：检查实体卡目录
            self.entity_dir = os.path.join(project_root, "00-实体卡")
            if not os.path.isdir(self.entity_dir):
                raise FileNotFoundError(
                    f"[ESM] 未指定 db_path 且找不到实体卡目录: {self.entity_dir}"
                )

    # ─── 数据库连接 ───────────────────────────────

    def _get_db(self) -> sqlite3.Connection:
        """懒加载数据库连接"""
        if self._db_conn is None and self.db_path:
            self._db_conn = sqlite3.connect(self.db_path)
        return self._db_conn

    def close(self):
        if self._db_conn:
            self._db_conn.close()
            self._db_conn = None

    # ─── 公共 API ─────────────────────────────────

    def find_card(self, entity_name: str) -> Optional[str]:
        """YAML 模式：查找实体卡片文件路径"""
        if self.db_path:
            # SQLite 模式不关心文件路径
            return entity_name if self._db_exists(entity_name) else None
        # YAML 模式
        for subdir in self.TYPE_DIR_MAP.values():
            path = os.path.join(self.entity_dir, subdir, f"{entity_name}.yaml")
            if os.path.isfile(path):
                return path
        thread_path = os.path.join(self.entity_dir, "thread", f"{entity_name}.yaml")
        if os.path.isfile(thread_path):
            return thread_path
        return None

    def load_entity(self, entity_name: str) -> Optional[dict]:
        """加载单个实体（兼容双模式）"""
        if self.db_path:
            return self._load_from_db(entity_name)
        # YAML 降级
        import yaml
        path = self.find_card(entity_name)
        if path is None:
            return None
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def load_entities(self, entity_names: List[str]) -> Dict[str, dict]:
        """批量加载实体"""
        result = {}
        for name in entity_names:
            card = self.load_entity(name)
            if card is not None:
                result[name] = card
            else:
                print(f"[ESM] ⚠️ 未找到实体: {name}")
        return result

    def list_all_entities(self) -> Dict[str, List[str]]:
        """列出所有实体"""
        if self.db_path:
            return self._list_from_db()
        # YAML 模式
        result = {}
        for entity_type, subdir in self.TYPE_DIR_MAP.items():
            dir_path = os.path.join(self.entity_dir, subdir)
            if not os.path.isdir(dir_path):
                continue
            names = [f[:-5] for f in os.listdir(dir_path) if f.endswith(".yaml")]
            if names:
                result[entity_type] = sorted(names)
        return result

    # ─── build_context_bundle（核心接口）─────────────

    def build_context_bundle(self, entity_names: List[str]) -> str:
        """
        加载实体并拼成上下文文本（给 Pass 1 / Pass 2 的 Prompt 用）。
        输出格式稳定，不依赖于后端存储。

        返回格式：
          ## {实体名}（类型）
          permanent: 身份/人设/色调摘要
          state: 当前位置/技能/认知/关系/心态
          ---
        """
        if self.db_path:
            return self._build_bundle_from_db(entity_names)

        # YAML 模式（原有逻辑）
        cards = self.load_entities(entity_names)
        lines = []
        for name, card in cards.items():
            entity_type = self._detect_type(card)
            lines.append(f"## {name}（{entity_type}）")

            perm = card.get("permanent", {})
            identity = perm.get("identity", {})
            tags = perm.get("lore_tag", [])
            palette = perm.get("description_palette", {})
            speech = perm.get("speech_style", {})

            lines.append(f"  身份: {identity.get('name', name)} / {identity.get('species', '?')} / {identity.get('title', '')}")
            if tags:
                lines.append(f"  人设: {' | '.join(tags[:4])}")
            if palette:
                p = f"{palette.get('primary','')}/{palette.get('texture','')} 比喻域:{','.join(palette.get('metaphor_domain',[]))}"
                lines.append(f"  色调: {p}")
            if speech:
                lines.append(f"  说话风格: {speech.get('type','')} {'|'.join(speech.get('traits',[]))}")

            state = card.get("state", {})
            loc = state.get("location", "?")
            health = state.get("health", {}).get("status", "?")
            mindset = state.get("current_mindset", "?")
            goal = state.get("current_goal", "?")
            skills = state.get("skills", {}).get("mastered", [])

            lines.append(f"  位置: {loc}")
            lines.append(f"  状态: {health}")
            lines.append(f"  心态: {mindset}")
            lines.append(f"  目标: {goal}")
            if skills:
                lines.append(f"  已掌握: {', '.join(skills[:6])}")
            lines.append("  ---")
        return "\n".join(lines)

    # ─── SQLite 内部实现 ──────────────────────────

    def _db_exists(self, name: str) -> bool:
        """检查 SQLite 中是否存在指定实体"""
        conn = self._get_db()
        if not conn:
            return False
        cur = conn.cursor()
        for tbl in ['characters', 'weirds', 'skills', 'items']:
            cur.execute(f"SELECT 1 FROM {tbl} WHERE name=? AND book_id=1", (name,))
            if cur.fetchone():
                return True
        return False

    def _load_from_db(self, name: str) -> Optional[dict]:
        """从 SQLite 加载实体为 dict（兼容 YAML 格式）"""
        conn = self._get_db()
        if not conn:
            return None
        cur = conn.cursor()

        # 尝试各表
        card = self._db_row_to_card(cur, 'characters', name, 'character')
        if card: return card
        card = self._db_row_to_card(cur, 'weirds', name, 'weird')
        if card: return card
        card = self._db_row_to_card(cur, 'skills', name, 'skill')
        if card: return card
        card = self._db_row_to_card(cur, 'items', name, 'item')
        if card: return card
        return None

    def _db_row_to_card(self, cur, table: str, name: str, entity_type: str) -> Optional[dict]:
        """将一行 SQLite 记录转为 YAML 兼容格式"""
        cur.execute(f"SELECT * FROM {table} WHERE name=? AND book_id=1", (name,))
        row = cur.fetchone()
        if not row:
            return None

        col_names = [d[0] for d in cur.description]
        vals = dict(zip(col_names, row))

        # 拼成 YAML 兼容格式
        card = {
            "permanent": {
                "identity": {
                    "name": name,
                    "species": entity_type,
                    "title": vals.get("brief", ""),
                },
                "lore_tag": [],
                "description_palette": {
                    "primary": "",
                    "texture": "",
                    "metaphor_domain": [],
                },
            },
            "state": {
                "location": "",
                "health": {"status": "normal"},
                "current_mindset": "",
                "current_goal": "",
                "skills": {"mastered": []},
                "relationships": [],
            },
            "source": "sqlite",
            "description": vals.get("description", ""),
        }

        # 填充各类型专属字段
        if entity_type == "character":
            ms = vals.get("mentality_stages", "[]")
            if isinstance(ms, str) and ms.startswith("["):
                try: card["state"]["mentality_stages"] = json.loads(ms)
                except: pass
            card["permanent"]["identity"]["species"] = "人类"
            card["state"]["current_mindset"] = vals.get("brief", "")
            card["importance"] = vals.get("importance", 5)

            # 获取技能（容错：skills表可能没有owner_id字段）
            try:
                cur.execute("""
                    SELECT name, type FROM skills 
                    WHERE owner_id=(SELECT id FROM characters WHERE name=? AND book_id=1)
                    ORDER BY acquire_chapter
                """, (name,))
                mastered = [f"{r[0]}({r[1]})" for r in cur.fetchall()]
            except sqlite3.OperationalError:
                mastered = []
            card["state"]["skills"]["mastered"] = mastered

            # 获取关系（容错：relationships表可能不存在）
            try:
                cur.execute("""
                    SELECT 
                        CASE WHEN r.target_type='character' THEN (SELECT name FROM characters WHERE id=r.target_id)
                             WHEN r.target_type='weird' THEN (SELECT name FROM weirds WHERE id=r.target_id) END,
                        r.relation_type, r.strength
                    FROM relationships r WHERE r.source_id=(SELECT id FROM characters WHERE name=? AND book_id=1)
                    ORDER BY r.strength DESC
                """, (name,))
                for tgt_name, rtype, strength in cur.fetchall():
                    card["state"]["relationships"].append({
                        "target": tgt_name,
                        "type": rtype,
                        "strength": strength,
                    })
            except sqlite3.OperationalError:
                pass

        elif entity_type == "skill":
            card["permanent"]["identity"]["title"] = vals.get("type", "")
            card["state"]["location"] = f"owner_id={vals.get('owner_id', '?')}"
            # 战斗表现
            for f in ['combat_style', 'combat_effect', 'combat_limits', 'combat_rhythm', 'power_scale']:
                if vals.get(f):
                    if "combat" not in card["state"]: card["state"]["combat"] = {}
                    card["state"]["combat"][f] = vals[f]

        elif entity_type == "item":
            card["permanent"]["identity"]["species"] = vals.get("item_type", "物品")
            card["state"]["location"] = f"owner_id={vals.get('owner_id', '?')}"
            card["state"]["current_state"] = vals.get("current_state", "active")

        elif entity_type == "weird":
            card["permanent"]["identity"]["title"] = f"{vals.get('tier','')}·{vals.get('danger_level','')}"
            card["state"]["health"]["status"] = vals.get("status", "active")
            for f in ['killing_pattern', 'weaknesses', 'origin']:
                if vals.get(f):
                    if "weird" not in card["state"]: card["state"]["weird"] = {}
                    card["state"]["weird"][f] = vals[f]

        return card

    def _list_from_db(self) -> Dict[str, List[str]]:
        """从 SQLite 列出所有实体"""
        conn = self._get_db()
        if not conn:
            return {}
        cur = conn.cursor()
        result = {}
        mapping = [
            ('character', 'characters'),
            ('skill', 'skills'),
            ('item', 'items'),
            ('weird', 'weirds'),
        ]
        for label, table in mapping:
            try:
                cur.execute(f"SELECT name FROM {table} WHERE book_id=1 ORDER BY name")
                names = [r[0] for r in cur.fetchall()]
                if names:
                    result[label] = names
            except:
                pass
        return result

    def _build_bundle_from_db(self, entity_names: List[str]) -> str:
        """从 SQLite 构建 context-bundle"""
        conn = self._get_db()
        if not conn:
            return "（数据库未连接）"
        cur = conn.cursor()

        lines = []

        # 先构建一个查询映射：哪些名字在哪个表
        for name in entity_names:
            card = self._load_from_db(name)
            if not card:
                continue

            entity_type = card["permanent"]["identity"]["species"]
            lines.append(f"## {name}（{entity_type}）")

            identity = card["permanent"]["identity"]
            lines.append(f"  身份: {identity['name']} / {identity['species']} / {identity['title']}")

            tags = card["permanent"].get("lore_tag", [])
            if tags:
                lines.append(f"  人设: {' | '.join(tags[:4])}")

            state = card["state"]
            loc = state.get("location", "?")
            health = state.get("health", {}).get("status", "?")
            mindset = state.get("current_mindset", "?")
            goal = state.get("current_goal", "?")
            mastered = state.get("skills", {}).get("mastered", [])

            lines.append(f"  位置: {loc}")
            lines.append(f"  状态: {health}")
            lines.append(f"  心态: {mindset}")
            lines.append(f"  目标: {goal}")
            if mastered:
                lines.append(f"  已掌握: {', '.join(mastered[:8])}")

            # 关系
            rels = state.get("relationships", [])
            if rels:
                rel_strs = [f"{r['target']}({r['type']}:{r['strength']})" for r in rels[:5]]
                lines.append(f"  关系: {'; '.join(rel_strs)}")

            # 战斗表现
            combat = state.get("combat", {})
            if combat:
                if combat.get('combat_style'): lines.append(f"  战斗风格: {combat['combat_style']}")
                if combat.get('power_scale'): lines.append(f"  战力: {combat['power_scale']}")
                if combat.get('combat_limits'): lines.append(f"  限制: {combat['combat_limits']}")

            # 诡异专属
            weird_info = state.get("weird", {})
            if weird_info:
                if weird_info.get('killing_pattern'): lines.append(f"  杀人规律: {weird_info['killing_pattern']}")
                if weird_info.get('weaknesses'): lines.append(f"  弱点: {weird_info['weaknesses']}")

            lines.append("  ---")

        return "\n".join(lines)

    # ─── 工具方法 ─────────────────────────────────

    NON_ENTITY_WORDS = {
        '黑色', '白色', '灰色', '红色', '光', '黑', '字', '词', '名称',
        '文字', '样式', '颜色', '声音', '画面', '图片', '照片', '相册',
        '屏幕', '界面', '图标', '按钮', '链接', '动画', '音效', 'UI',
        '字体', '等宽字体', '提示', '翻译', '来源', '调试', '原始信息',
        '详情', '详细说明', '即时消息', '痕迹', '底层', '实体名', '来源分析',
        '手指', '大脑', '组合', '截屏',
        '数据删除', '残留', '普通残留', '高品质残留', '资源',
        '信息', '格式', '方向', '位置', '目标', '方式', '模式',
        '客厅', '楼道', '房间', '小区', '停车场', '区域', '门',
        '卧室', '阳台', '走廊', '窗户', '街道', '路灯', '墙壁',
    }

    @staticmethod
    def extract_entity_references(text: str) -> List[str]:
        """从文本中提取所有 {实体名} 引用（已过滤非实体词）"""
        matches = re.findall(r'\{([^}]+)\}', text)
        seen = set()
        result = []
        for m in matches:
            if m not in seen and m not in EntityLoader.NON_ENTITY_WORDS:
                seen.add(m)
                result.append(m)
        return result

    @staticmethod
    def _detect_type(card: dict) -> str:
        """从卡片内容推断实体类型"""
        perm = card.get("permanent", {})
        identity = perm.get("identity", {})
        species = identity.get("species", "")
        lore_tags = perm.get("lore_tag", [])

        if "老狗" in str(lore_tags) or species == "人类" or "speech_style" in perm:
            return "角色"
        if "type" in perm:
            t = perm.get("type", "")
            if any(k in t for k in ["技能", "传奇", "盗贼"]): return "技能"
            if any(k in t for k in ["金手指", "穿越"]): return "物品"
            if any(k in t for k in ["城市", "城区", "空间"]): return "地点"
            if any(k in t for k in ["伏笔", "悬空", "背景"]): return "伏笔"
        if "cause_of_death" in card.get("state", {}):
            return "角色"
        return "其他"
