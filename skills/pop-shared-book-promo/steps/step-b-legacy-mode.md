# 模式 B：旧模板管线（向后兼容 ⚠️ Deprecated）

当不需要设计哲学和 PRD 时，直接用旧模板快速出稿：

```bash
python3 scripts/generate.py --mode comic --input examples/scenes.json --output ../书名_四格漫画.html
python3 scripts/generate.py --mode scroll --input examples/profile.json --output ../书名_人物画卷.html
python3 scripts/generate.py --mode scenes --input examples/scenes.json --output ../书名_名场面.html
python3 scripts/generate.py --mode quote --input examples/quotes.json --output ../书名_金句卡.html
python3 scripts/generate.py --mode gallery --input examples/characters.json --output ../书名_立绘画廊.html
```

## 参数说明

| 参数 | 必填 | 说明 |
|:-----|:----:|:------|
| `--mode` | ✅ | image / comic / scroll / scenes / quote / gallery |
| `--backend` | ❌ | seedream（默认）或 openrouter |
| `--input` / `-i` | ⚠️ | 输入 JSON（模板模式需要） |
| `--output` / `-o` | ✅ | 输出路径 |
| `--prompt` / `-p` | ⚠️ | 出图提示词（仅 image 模式） |
| `--model` | ❌ | 图像模型 ID（默认: doubao-seedream-5-0-260128） |
| `--max-items` | ❌ | 前 N 项，冒烟测试 |
| `--reference-dir` | ❌ | 角色参考图目录 |
| `--save-assets` | ❌ | 同时保存图片到目录 |
