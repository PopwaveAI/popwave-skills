# Step 4：活记忆压缩

> 管线: pop-writer-v3-arc v1.2.0
> 消费: 活记忆.yaml（最后baseline + 之后全部event）
> 产出: 压缩后的活记忆.yaml + 压缩记录

## 读什么

- `活记忆/活记忆.yaml`（全量：最后baseline + 之后全部event）
- `项目总控.md`（当前章号，判断是否达到压缩条件）

## 做什么

### 1. 压缩条件检查

| 条件 | 是否压缩 |
|:-----|:---------|
| 距上次压缩 >=20章（event累积>=20条） | 执行压缩 |
| 距上次压缩 <20章 | 跳过压缩，记录"未达压缩条件" |
| 本次校准触发了严重回退 | 先执行回退，回退后再评估压缩条件 |

### 2. 压缩执行（如达到条件）

压缩策略：读最后一个baseline + 之后全部event → 合并成新baseline → 删旧baseline及其后event → 追加新baseline。

#### 2a. 读取最后一个baseline

找到entries中最后一个type=baseline的条目，记录其chapter号。

#### 2b. 读取之后全部event

收集该baseline之后的所有type=event条目。

#### 2c. 逐组件合并

| 组件 | 合并策略 |
|:-----|:---------|
| 种子追踪(seeds) | 合并所有event的seeds_added，保留最终状态（活跃/已回收/超期），去重 |
| 压力状态(pressure) | 取最后一个event的pressure值（覆盖式更新） |
| 角色状态(characters) | 合并所有event的character_changes，取最终状态 |
| 世界规则(world_rules) | 追加所有event的world_rules_added（只增不改，去重） |
| 节奏日志(rhythm_log) | 保留全部event的rhythm_entry（历史记录，不压缩） |
| 战力曲线(power_curve) | 合并所有event的power_entry（时间序列，全部保留） |
| 目的地进度(destinations) | 取最后一个event的destination_updates（覆盖式更新） |

#### 2d. 生成新baseline

```yaml
- type: baseline
  chapter: {当前章号}
  timestamp: {当前时间}
  seeds: {合并后的种子追踪}
  pressure: {合并后的压力状态}
  characters: {合并后的角色状态}
  world_rules: {合并后的世界规则}
  rhythm_log: {全部节奏日志}
  power_curve: {全部战力曲线}
  destinations: {合并后的目的地进度}
```

#### 2e. 替换

1. 删除旧baseline及其后全部event
2. 追加新baseline
3. 更新metadata：last_compacted_at = {当前章号}

### 3. 压缩后验证（红线❌3）

逐组件校验新baseline完整性：

| 检查项 | 失败动作 |
|:-------|:---------|
| 七组件全部存在（seeds/pressure/characters/world_rules/rhythm_log/power_curve/destinations） | 缺组件=回滚压缩，恢复旧数据 |
| 每组件数据非空（rhythm_log/power_curve允许有历史数据） | 空组件=回滚压缩 |
| 节奏日志章号连续无断 | 断章=回滚压缩 |
| 战力曲线章号连续无断 | 断章=回滚压缩 |
| 文件大小 5-15KB | 超出范围=检查是否有冗余数据 |

### 4. 压缩失败处理

如果验证不通过：
1. 回滚：恢复压缩前的活记忆.yaml（从备份）
2. 记录失败原因
3. 不执行压缩，下次校准时重试
4. 在校准报告中标记"压缩失败，需人工检查"

## 门禁

| 检查项 | 失败动作 |
|:-------|:---------|
| 压缩后七组件完整性验证通过（红线❌3） | 验证失败=回滚压缩 |
| 压缩后文件5-15KB | 超范围=检查冗余，必要时人工干预 |
| 压缩前备份活记忆.yaml | 无备份=先备份再压缩 |
| metadata.last_compacted_at 已更新 | 未更新=补更新 |

## 产出

1. 压缩后的 `活记忆/活记忆.yaml`（新baseline替换旧baseline+event）
2. 压缩记录（填入校准报告草稿）：

| 项目 | 内容 |
|:-----|:-----|
| 压缩前章号范围 | ch{旧baseline章号}-ch{当前章号} |
| 压缩前文件大小 | XX KB |
| 压缩后文件大小 | XX KB |
| 合并event数量 | N条 |
| 七组件完整性 | ✅ 全部通过 |
| 压缩状态 | 成功 / 未达条件 / 失败 |

### 5. 校准报告落盘（红线❌4）

所有四步完成后，将校准报告草稿整理为正式报告：
1. 使用 `templates/弧线校准报告-模板.md` 格式
2. 落盘到 `弧线校准报告/arc-{XX}.md`（XX=校准序号）
3. 更新 `项目总控.md`：弧线计数+1

---
✅ 校准完成。下一步：返回 `pop-writer-v3-emerge` 继续涌现写作环。
