> ⚠️ **废弃 — 勿引用** 本文件所属 skill 已被重构/删除。agent 不应加载此文件。
> 所有活跃 skill 位于 skills/pop-novel-*

---
name: novel-agent-pro
description: 鍏ㄩ摼璺綉鏂囧垱浣滅郴缁燂紝鍖呭惈鎷嗕功/寮€涔?鍓ф儏鏋舵瀯/姝ｆ枃鍐欎綔/QC璐ㄦ/HTML鍙戝竷绛夊畬鏁寸绾裤€侷nvoke when user wants to write a novel from scratch or needs full writing pipeline support.
version: 3.3.0
---

# novel-agent-pro 鈥?瀛怱kill 绱㈠紩鎬荤翰

> 鐗堟湰锛?*v4.2** 路 鏇存柊锛?026-06-03
> 鐢ㄩ€旓細agent 璺敱绱㈠紩銆傛敹鍒?鍐欑珷鑺?鎷嗕功/寮€涔?绛変换鍔?鈫?鏌ユ鏂囦欢鐨勬ā鍧楀垝鍒?鈫?纭畾瀛?Skill 璺緞銆?

---

## 涓€銆佺绾挎€昏锛堝叚闃舵 路 14 椤硅緭鍏ュ寘锛?

```
Phase 0: 鎻愬墠瀹屾垚鐨勮瀹氾紙寮€涔﹂樁娈碘€?project-bootstrap锛?
  鈹斺攢鈹€ 鎷嗚В鎶ュ憡 / 璁惧畾灞?/ 澶х翰灞傛牎鍑?
  鈹斺攢鈹€ Boss璁捐 + 鏁板€间綋绯?+ 閿氬畾绔犲簱 + 缁忛獙鏃ュ織
        鈹?reader_profile 绌块€忓叏绠＄嚎
        鈻?
Phase 1: Director Agent 鈫?璁捐璇存槑 + 鍐崇瓥鏃ュ織 鈫?猸?澶х翰灞俀C
Phase 2: Pass 1 楠ㄦ灦 Agent 鈫?浜嬪疄楠ㄦ灦 鈫?猸?楠ㄦ灦灞俀C
Phase 3: ESM before锛堥浂LLM路14椤硅緭鍏ュ寘锛夆啋 bundle.md
Phase 4: Pass 2 娓叉煋 + 鍐欏悗鑷瘎 鈫?姝ｆ枃 chXXX.md
Phase 5: 猸?QC Agent 路 涓夊眰浠嬪叆锛堝ぇ绾?楠ㄦ灦/姝ｆ枃锛?
Phase 6: ESM after锛堥浂LLM锛夆啋 state_changelog + 鍏ㄥ眬鎽樿
```

---

## 浜屻€佹ā鍧楀垝鍒嗭紙鎸夋祦姘寸嚎锛?

鏀跺埌鐢ㄦ埛璇锋眰鏃讹紝鏍规嵁鍏抽敭璇嶈矾鐢卞埌瀵瑰簲瀛?Skill銆?

### 璋冪爺灞?
| 瀛?Skill | 璺緞 | 鍏抽敭璇?|
|:---------|:-----|:-------|
| cnovel-research | `skills/cnovel-research/` | 璋冪爺銆佹悳绱€佺爺绌?|
| book-opinion-tracker | `skills/book-opinion-tracker/` | 鑸嗘儏銆佷功璇勩€佸彛纰?|

### 寮€涔﹀惎鍔?
| 瀛?Skill | 璺緞 | 鐗堟湰 |
|:---------|:-----|:-----|
| project-bootstrap | `skills/skill-project-bootstrap/` | v2.9 |
| book-deconstructor | `skills/skill-book-deconstructor/` | v4.8 |

### 鍓ф儏璁捐
| 瀛?Skill | 璺緞 | 鐗堟湰 |
|:---------|:-----|:-----|
| plot-architecture | `skills/skill-plot-architecture/` | v2.7 |
| opening-arc | `skills/skill-opening-arc/` | v1.1 |

### 姝ｆ枃鍐欎綔锛堚槄 鏍稿績锛?
| 瀛?Skill | 璺緞 | 鐗堟湰 |
|:---------|:-----|:-----|
| emergent-writer | `skills/skill-emergent-writer/` | v9.3 路 鍏樁娈电绾?|

### 璐ㄦ涓庡彂甯?
| 瀛?Skill | 璺緞 | 鐗堟湰 |
|:---------|:-----|:-----|
| qa-payoff | `skills/skill-qa-payoff/` | v0.4.1 |
| html-renderer | `skills/skill-emergent-writer/html-renderer/` | v1.3 |

### 鍏朵粬
| 瀛?Skill | 璺緞 | 鐗堟湰 |
|:---------|:-----|:-----|
| market-test | `skills/skill-market-test/` | v1.2 |
| _continuation | `skills/_continuation/` | 缁啓閫傞厤 |
| horror-game-writer | `skills/skill-horror-game-writer/` | 鈥?|

---

## 涓夈€佸叏娴佺▼璐€?

```
Step 1: 鎷嗕功锛坆ook-deconstructor锛夆啋 鎷嗚В鎶ュ憡 + 閿氬畾绔犲簱
Step 2: 寮€涔︼紙project-bootstrap锛夆啋 L0-L1璁惧畾 + reader_profile + 鏁板€间綋绯?
Step 3: 榛勯噾涓夌珷锛坥pening-arc锛夆啋 ch001-ch003
Step 4: 骞曠翰璁捐锛坧lot-architecture锛夆啋 act-XX.yaml
Step 5: 姝ｆ枃寰幆锛坋mergent-writer锛夆啋 Director 鈫?楠ㄦ灦 鈫?ESM 鈫?娓叉煋 鈫?QC 鈫?鐘舵€佹洿鏂?
```

## 鍥涖€佺増鏈?

鍚勬ā鍧楄缁嗙増鏈€侀摼璺璁°€佽兌姘翠唬鐮佹柟妗?鈫?鍙傝 `references/`

