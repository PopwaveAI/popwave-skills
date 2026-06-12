# CHANGELOG — pop-novel-creative

## v1.3.0 — 2026-06-12

### 剥离数据采集层 → world
- Phase 0.6（跨域素材）和 Phase 0.7（拆书融合）移至 pop-novel-world 的 Phase W0/W1
- creative 在样品签字后使命完成——不负责采集 world 用的数据
- 交接包精简为：故事引擎.md + 样品签字 + 主角设计笔记 + 参考书策略
- world 的新增红线：跨域素材始终强制，拆书融合有对标书时强制

---

## v1.2.0 — 2026-06-12

### Phase 0：方向 sketch 轻量化 + yaml 退场
- 方向产出从"三层 heavy brief"改为"轻量 sketch（碰撞+钩子+第一画面+基调，~150字）"
- 用户选完方向后才深化为完整的故事引擎.md（不浪费时间深挖没选的方向）
- **story-engine.yaml 退场** — 全部产出改为 .md 格式，叙事优先、人可读
- 红线 ❌7 从"卖点验证可复述"改为"故事引擎可被十分钟读完"
- 交接包更新：`故事引擎.md` 替代 `story-engine.yaml`

### Phase 0.3：参考书甄别 → 参考书策略
- 定位从"自己做拆书"改为"deconstructor 的策略层"
- 新流程：从碰撞点推导验证需求 → 形成观察清单（映射到 deconstructor T维度）→ 触发 deconstructor Lv1 → 差异化决策 → 反哺宪法
- 产出从 `_参考书分析/{书名}.md` 改为 `观察清单+差异化.md`

### Phase 0.4：金手指设计 → 主角设计
- 金手指降为主角的子维度，不再独立 Phase
- 新增"唯一性"作为第四维（必填）——替代原来的"能力/金手指"
- 唯一性四级评估从"能力评估"改为"主角资格检验"：L1核心差异 / L2约束 / L3不可替代性 / L4叙事驱动
- 任何题材都必走唯一性四级评估。"金手指"只是修真/系统类下唯一性的载体之一

### 其他
- 红线 ❌1: story-engine.yaml v3 → 故事引擎.md
- 红线 ❌5: 金手指四级评估 → 主角四维完整（唯一性必填）
- 下游 world 同步更新所有 yaml→md 引用

---

## v1.1.0 — 2026-06-12

### Phase 0 重构：追问 → 元素融合 SOP
- 从"接住+追问 2-3 轮"改为"碎片分析+元素联想+碰撞评级+方向 brief 生成"
- 新增元素融合 5 步 SOP（解吸→拆规则→找碰撞点→落主角→方向 brief）
- 新增方向 brief 模板（宏观/卖点/微观三层咬合）
- 新增碰撞强度评级（★☆☆弱碰撞 ★★☆中等 ★★★强碰撞）
- story-engine v3 新增 `fusion_method` / `colliding_elements` / `collision_point` 字段
- 用户交互从"被审问"变为"在 2-3 个完整提案中选择"

---

## v1.0.0 — 2026-06-12

### 初始分叉
- 从 pop-novel-bookstrap v4.1.0 分叉
- 剥离 L1 设定层（Phase 1-1.5）→ 移入 pop-novel-world
- 剥离数值体系（Phase 3-5）→ 移入 pop-novel-world
- 剥离起点/终点快照（Phase 6-7）→ 移入 pop-novel-world
- 新增 Phase 0.5 样品试读（核心闸门）
- story-engine 升级至 v3（constitutional_bounds + selling_point_validation）
- 管线位置变更：deconstructor → creative → world
