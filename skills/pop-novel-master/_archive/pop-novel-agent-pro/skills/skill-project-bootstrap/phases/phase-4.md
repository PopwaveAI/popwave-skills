# Phase 4：reader_profile 嵌入 project.yaml

**目标**：将读者画像字段嵌入 project.yaml，确保设定层始终对齐目标读者。

**条件**：project.yaml 已创建（Phase 3）。

## 执行步骤

1. **从 PRD 中提取读者画像**
   - 人口统计：年龄/性别/阅读场景
   - 阅读偏好：节奏/篇幅/元素
   - 爽点敏感度：按类型量化（1-5分）
   - 弃书阈值：前3章/前10章

2. **嵌入 project.yaml**
   ```yaml
   reader_profile:
     demographic:
       age_range: "18-30"
       reading_scenario: "commute"
     reading_preference:
       pace: "fast"
       chapter_length: "2000-3000"
     drop_threshold:
       first_3_chapters:
         - "no_power_up_in_3_chapters"
   ```

3. **设定-读者对齐检查**
   - 逐项检查 L1 设定与读者画像无冲突
   - 有冲突则标记调整方向
