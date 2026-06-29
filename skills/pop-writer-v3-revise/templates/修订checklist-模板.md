# 修订记录模板

> revise 使用。只响应用户目标，不做默认全量质检。

## 一、修订目标

| 项 | 内容 |
|:---|:-----|
| 用户要求 | |
| 修订模式 | 轻修 / 重写 / 压缩 / 扩写 |
| 风险 | 无 / 可能影响运行日志结算 / 可能影响设定账本 |

## 二、不可改写项

```markdown
## 事件链
- 

## 本章结算
- 

## 章末推力
- 

## 禁止漂移设定
- 
```

## 三、修订后正文

```markdown
# chXXX · {标题}

{正文}
```

## 四、修订记录

```yaml
revise_record:
  mode: light|rewrite|compress|expand
  user_goal: ""
  unchanged_settlement:
    - ""
  setting_ledger_touched:
    - ""
  style_dna_loaded: true
  risk: none
```

## 五、自检

- [ ] 已响应用户明确要求。
- [ ] 未改变运行日志结算。
- [ ] 未新增未入账重大设定。
- [ ] 未越过章末推力。
- [ ] 文风 DNA 已完整读取并体现。
