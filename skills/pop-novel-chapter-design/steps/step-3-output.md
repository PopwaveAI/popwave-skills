# Step 3：产出与状态更新

> 管线: pop-novel-chapter-design v1.4
> 模板: `templates/fact-skeleton.md` + `templates/character-card.md`

---

## 目的

组装 Step 2 的事件链和角色 after 状态，写入最终文件，更新全局状态。

---

## 产出

### 1. 写入 `03-写作资产/chXXX-事实骨架.md`

按 `templates/fact-skeleton.md` 格式写入：
- 基础信息（幕/章号/标题/核心目的/场景类型/爽点等级/字数）
- 跨章弧线（如有）
- 事件链（12-30 个事件，每个含地点/角色/内容/情绪/信息释放/估计字数）
- 情绪节拍（起点→推进→高潮→终点）
- 信息释放落地清单
- 钩子
- 与上章衔接

### 2. 写入 `03-写作资产/chXXX-登场人物卡.md`

按 `templates/character-card.md` 格式写入：
- 每个出场角色的 before/after 状态
- 配角的叙事功能 + 台词风格
- 角色关系动态
- 角色出场分布

### 3. 更新 `00-总控/entity-snapshot.yaml`

根据本章所有角色的 after 状态更新：
- 角色状态（等级/位置/装备/心理）
- 事件日志（追加本章事件摘要）
- flags（新增/更新/移除）
- timeline
- `_meta.total_chapters + 1`

---

## 产出自检

- [ ] 事实骨架中每个事件的「参与角色」在 volume-XX.md §三 中存在
- [ ] 事实骨架中每个事件的「地点」在 volume-XX.md §三 中存在
- [ ] 登场人物卡中每个角色的 before 状态与 entity-snapshot 一致
- [ ] entity-snapshot 已正确更新
- [ ] constitution 红线全部通过
- [ ] 骨架文件有版本元数据
- [ ] 人物卡文件有版本元数据
