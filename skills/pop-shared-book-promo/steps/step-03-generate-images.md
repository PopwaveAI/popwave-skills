# Step 3：生成图片

| 项目 | 内容 |
|:-----|:------|
| 读什么 | PRD 中的 image_prompt 列表 |
| 做什么 | 用 `generate.py` 逐张生图 |
| 产出 | `.png` 图片文件 + data URL |

## 执行

```bash
python3 scripts/generate.py --mode image \
  --prompt "Chinese xianxia novel scene: ..." \
  --output assets/scene1.png
```

## 门禁清单

- [ ] 每张图片生成成功
- [ ] 图片无模糊/变形
- ❌ 生图失败 → 检查 API Key 是否过期，重试 3 次，仍失败则报错。
