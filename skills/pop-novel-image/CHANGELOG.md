# CHANGELOG

## v1.0.0 — 2026-08-01

### 新增
- 创建 `pop-novel-image` skill，定位为营销专家skill群的通用文生图引擎+画风DNA库共享基座
- 迁移36种画风DNA库（`references/style-dna-library.json`），含3光照模板+2构图模板+兼容性矩阵
- 创建 `references/seedream-prompt-guide.md`：6段式提示词结构（默认）+ V3结构化公式（备选）+ 高精度4块结构（商业级备选）
- 创建 `references/lighting-composition-templates.md`：3光照模板+2构图模板+三分法兼容性矩阵
- 创建3个step文件：画风选择→提示词组装→执行生成
- 复制 `scripts/generate.py`（Seedream/Seedance API调用脚本）

### 定位
- 独立执行纯文生图任务
- 作为cover/oc/comic skill的共享画风层引用源
- 不替代各skill的结构层和功能层
