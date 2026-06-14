# Step 1.5-2: 识别内容类型 + 提取文本

## 第二步：识别内容类型 + 提取文本

询问用户内容类型：

> 这些资料是什么类型？
> 1. **技术类** — 含代码块、表格、公式（编程书/论文/架构指南）
> 2. **文字类** — 主要是散文，表格/代码很少（管理/效率/叙事非虚构）
> 3. **不确定** — 我用快速方法，质量有限时提醒你

- 选 1 → `BOOK_TYPE=technical`（用 Docling，~1.5s/页）
- 选 2 或 3 → `BOOK_TYPE=text`（用最快提取器）

运行提取脚本：

```bash
python scripts/extract.py <INPUT_PATHS> --mode <BOOK_TYPE> --install-missing ask
```

产出：
- `<tempdir>/book_skill_work/full_text.txt` — 合并提取文本
- `<tempdir>/book_skill_work/metadata.json` — 统计数据

**预检环境：** `python scripts/extract.py --check` 打印各格式提取器安装状态。

❌ 门禁：**必须在提取前询问内容类型。** 选错 `BOOK_TYPE` 会导致技术书的表格/代码丢失或文字书浪费 Docling 时间 → 退回重选。
