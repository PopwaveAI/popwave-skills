# CHANGELOG

## v1.4.2 — 2026-08-04

### 出图尺寸硬上限（防止报价翻倍）

- `steps/step3-generate.md` 尺寸表新增铁律：所有出图总像素 ≤ 236 万（Seedream 5.0 Pro 计费临界，超限报价翻倍），上表全部安全（最大 1500x1500=225 万）；`generate.py` 内置 `assert_size_safe` 校验，超限报错中止

## v1.4.1 — 2026-08-04

### 升级：画风定标改为"画风×项目角色联合测试"

老板实测发现固定中性素材测不出"画风能否撑起项目角色"（玄鉴仙族用中性"现代青年+木屋"测画风，测不出"黑金甲衣+金瞳"主角的适配度）。画风定标默认用项目主角做测试素材：

- `step4-style-calibrate.md` 改为画风×项目角色联合测试：用 `--character`（项目角色描述）+ `--character-image`（定妆图/OC图，图生图保证角色一致）传项目真实角色，验证"画风能否撑起这个角色"
- 仅排查"画风本身是否被执行"时才用中性素材（`--character` 不传）
- 测试素材章节新增"项目主角"缺省（Phase 0 未定角色时回退标准角色）
- 同步更新 SKILL.md Step 4 描述、铁律 ❌5（变量隔离扩展到"测试角色固定为项目主角"）

## v1.4.0 — 2026-08-04

### 新增：画风定标走固定脚本（固定 SOP + 并发批量）

把画风定标从"单张组装+单张生成+单张复现"改为"固定脚本并发批量"，杜绝每次测试全新设计、不稳定、慢：

- `step4-style-calibrate.md` 改为走固定脚本 `../pop-visual-shared/scripts/batch_test.py`：固定测试素材（变量隔离）+ 固定 6 段式模板 + 并发批量（默认 8 线程）+ 自动 `pe-log.json`
- 变体从 DNA 库按画风名批量取（`--style-names`），或 `--config` 精调（`--config` 只改一个子维度回炉）
- 稳定复现验证改为同 seed 重跑脚本，输出按 `seed-{seed}` 分级，天然复现对比
- SKILL.md 更新：Step 4 描述、铁律 ❌9、速查表（batch_test.py）
- 红线：定标必须走固定脚本，禁止现场手写提示词、单张串行

## v1.3.0 — 2026-08-04

### 新增：Pinterest 参考图单张锚定 + 稳定复现工作流

- Step 1 新增 **Pinterest 参考图搜索（单张锚定）**：选定画风后搜 1 张最符合画风的参考图，落盘 `素材/ref-cache/`，路径记决策.md（一次搜索、全程复用）
- Step 4 新增 **稳定复现验证（核心）**：同 seed + 同提示词复现对比，确认画风稳定而非单次运气，未稳定复现不冻结
- 画风冻结时记录 **seed + 参考图路径**，下游复用同 seed 保证画风不漂移
- 明确参考图是"图资产"（整图 image 参数复用），不靠精确分离公式提炼文字
- SKILL.md 更新：Step 1/4 描述、铁律 ❌7/❌8、速查表、跨skill引用协议第7条
- 参考图复用粒度：**单张锚定**（老板拍板）

## v1.2.0 — 2026-08-04

### 新增：画风定标（Pipeline 语境下必做）

- 新增 `steps/step4-style-calibrate.md`：用**固定测试素材**渲染 1 张画风定标图（变量隔离）
- 画风第一次被眼睛看到，验证 DNA 是否被 Seedream 准确执行
- 新增 🚪 **画风定标验收门禁**（辨识度/配色/光影/无文字）
- 用户认可 → **冻结画风三字段为基线资产**（`素材/风格/画风决策.md` 标 `✅ 已认可`）
- 未认可 → 回炉微调 DNA 片段，不冻结、不放行下游
- SKILL.md 更新：新增 Step 4、铁律 ❌5/❌6、速查表、跨skill引用协议第6条
- 独立纯文生图时跳过本步（Step 1→2→3 直接出图）

## v1.1.0 — 2026-08-04

### 接入共享底层资产层（瘦身清理）

- 删除本地 `scripts/generate.py` / `references/seedream-prompt-guide.md`，统一引用共享层 `pop-visual-shared`
- 6段式提示词结构迁移到共享库 `seedream-prompt-guide.md` §一（本 skill 保留 `style-dna-library.json` 与 `lighting-composition-templates.md` 域资产）
- SKILL.md 速查表 + step 文件引用路径切到 `../pop-visual-shared/...`

## v1.0.0 — 2026-08-01

### 新增
- 创建 `pop-visual-style` skill，定位为营销专家skill群的通用文生图引擎+画风DNA库共享基座
- 迁移36种画风DNA库（`references/style-dna-library.json`），含3光照模板+2构图模板+兼容性矩阵
- 创建 `references/seedream-prompt-guide.md`：6段式提示词结构（默认）+ V3结构化公式（备选）+ 高精度4块结构（商业级备选）
- 创建 `references/lighting-composition-templates.md`：3光照模板+2构图模板+三分法兼容性矩阵
- 创建3个step文件：画风选择→提示词组装→执行生成
- 复制 `scripts/generate.py`（Seedream/Seedance API调用脚本）

### 定位
- 独立执行纯文生图任务
- 作为cover/oc/comic skill的共享画风层引用源
- 不替代各skill的结构层和功能层
