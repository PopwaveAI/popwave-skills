# 起点skill群测试项目

## 概述
起点skill群组三层骨架重构后的全链路测试。通过DeepSeek API直接调用skill（读SKILL.md+step文件拼成system prompt），验证重构后的起点skill群组（pipeline v1.1.0 + seed v8.1.0 + world v2.0.0 + character v1.0.0 + plot v4.0.0 + write v3.0.0 + review v3.0.0）能否正常产出。

## 测试链路
```
Phase 1: seed骨架层（1d力量体系+1e动力引擎+1f自洽）→ 骨架.md
Phase 2: seed主角层（2a主角+2b金手指+2c爽感矛盾）→ 主角设计.md
Phase 1续: seed创意发散+故事纲领+黄金首章 → 创意.md+ch001
Phase 3: world消费骨架生长血肉 → 全书设定
Phase 3.5: character建角色库 → 角色库.md
Phase 4: plot四层结构剧情白描 → 剧情白描.md
Phase 5: write写ch001正文 → ch001.txt
Phase 6: review四维审核 → review-ch001.md
```

## API配置
- API: DeepSeek deepseek-v4-flash
- 落盘规范: input+output+meta三件套

## R1测试
- 赛道: 仙侠修真
- 参考书: 深渊主宰（D&D数据面板流派）
- 脚本: R1/run_r1.py
