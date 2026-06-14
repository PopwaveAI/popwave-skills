# Step 3：产出与状态更新

> 管线: 09-pop-novel-chapter-design v1.5
> 模板: `templates/fact-skeleton.md`（已合并，含事实骨架 + 登场人物卡）

## 目的

组装 Step 2 的事件链和角色 after 状态，写入**一个设计包文件**，更新全局状态。

---

## 产出

### 1. 写入 `写作资产/设计包/chXXX-设计包.md`

按 `templates/fact-skeleton.md` 格式写入：
- 基础信息（幕/章号/标题/核心目的/场景类型/爽点等级/字数）
- 跨章弧线（如有）
- **登场人物**（主角 before/after 状态 + 配角表 + 关系动态 + 出场分布）
- 事件链（12-30 个事件，每个含地点/角色/内容/情绪/冲突层次/信息释放/估计字数）
- 情绪节拍（起点→推进→高潮→终点）
- 信息释放落地清单
- 钩子
- 与上章衔接

### 2. 更新 `00-总控/entity-snapshot.yaml`

根据本章所有角色的 after 状态更新：
- 角色状态（等级/位置/装备/心理）
- 事件日志（追加本章事件摘要）
- flags（新增/更新/移除）
- timeline
- `_meta.total_chapters + 1`

---

## 产出自检

- [ ] 设计包文件中每个事件的「参与角色」在 `chapters[N].登场角色` 中存在
- [ ] 设计包文件中每个事件的「地点」在 volume-XX.md §三 中存在
- [ ] 每个人物的 core_desire 从 `状态/角色/{角色名}-角色卡.md` 取（不是凭记忆）
- [ ] 登场人物 before 状态与 entity-snapshot 一致
- [ ] entity-snapshot 已正确更新
- [ ] Canvas 字段（chapters[].canvas 约束）全部通过
- [ ] ◆小爽点事件 ≥ 5 个（干脆斩杀/升级/打脸/梗植入。详见 `references/payoff-guide.md` §二）
- [ ] ★中爽点事件 ≥ 1 个（读者读完认知有变化？详见 `references/payoff-guide.md` §三）
- [ ] 设计包文件有版本元数据
