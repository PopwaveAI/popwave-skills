# Phase 4：reader_profile 确认校对（降级版）

## 前置条件
Phase 0 已完成（story-engine.yaml 已产出并嵌入 project.yaml）。

## 说明
reader_profile 已在 Phase 0 直出并嵌入 project.yaml。本步仅做确认校对，不重复提取。

## 执行步骤

### 1. 加载已嵌入的 reader_profile
从 project.yaml 中读取 reader_profile 字段。

### 2. 对齐核查

| 检查项 | 确认 |
|:-------|:----:|
| L1 设定复杂度与 reader_profile 的阅读偏好匹配？ | [ ] |
| 爽点覆盖了 reader_profile 中高敏感领域？ | [ ] |
| L1 设定无违反 drop_threshold 的设定（如高强度用户不应有超长铺垫）？ | [ ] |
| reader_profile 与 Phase 0 产出时一致，未被中间相位覆盖？ | [ ] |

### 3. 差异处理
- 全部通过 → 完成
- 存在不匹配 → 输出差异说明，返回 Phase 2 对应 L1 文件调整
