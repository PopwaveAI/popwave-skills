> ⚠️ **废弃 — 勿引用** 本文件所属 skill 已被重构/删除。agent 不应加载此文件。
> 所有活跃 skill 位于 skills/pop-novel-*

---
name: project-bootstrap
display_name: "寮€涔﹀惎鍔?
category: bootstrap
scenario: design
mode: project
recommended: 1
tags: ["寮€涔?, "璁惧畾", "鍒濆鍖?, "楠ㄦ灦"]
fidelity: production
description: "寮€涔﹀惎鍔?v2.9銆備粠L0鐏甸瓊瀵归綈鈫掓牳蹇冨崠鐐规繁搴︾爺绌垛啋璺ㄥ煙绱犳潗鑱氬悎锛堝己鍒讹級鈫扡1-L3鍒嗗眰璁惧畾鈫扡1娣卞害灞曞紑锛堥€愮瘒鎵╁啓+浜ゅ弶鍏宠仈锛夆啋绋冲畾鎬ф楠屸啋椤圭洰楠ㄦ灦鍒涘缓銆?
version: v2.9
novel_agent_version: v3.3
orchestration:
  preflight: []
  dependencies: []
  inject_context: []
  subagent_required: true
directory: skill-project-bootstrap

produces:
  - 00-鍘熷璁惧畾/L0-浜у搧灞?PRD.md
  - 00-鍘熷璁惧畾/_鍙傝€冧功鍒嗘瀽/{涔﹀悕}.md
  - 00-鍘熷璁惧畾/L1-鍏冭瀹氬眰/01-06.md
  - 00-鍘熷璁惧畾/world-stability-check.md
  - 02-澶х翰/鍗?1/锛堝湴鐞?鍔垮姏/瑙掕壊/鍓ф儏/瑁呭/鐖界偣璁捐锛?
  - 02-澶х翰/L3-瑙掕壊灞?锛堣鑹插崱锛?
  - 00-鎬绘帶/project.yaml chapter-state.yaml project-status.html
  - 00-鎬绘帶/鏁板€间綋绯?锛坈ombat_capability/monster_rank_map/act_rank_schedule锛?
  - 03-姝ｆ枃/
  - 04-鏁版嵁搴?novel.db
  - constitution.yaml
---

# 寮€涔﹀惎鍔?鈥?鍒濆鍖栫绾?

> 鐗堟湰锛歷2.9 | 鏃ユ湡锛?026-06-03 | 鍒嗙被锛歜ootstrap | 鎵ц椤哄簭锛歅hase 1

## 浠€涔堟椂鍊欎娇鐢?

| 鍦烘櫙 | 璇存槑 |
|------|------|
| **鏂颁功寮€鍧?* | 浠庨浂鍒颁竴鎼缓瀹屾暣鐨勫皬璇撮」鐩鏋?|
| **鍒涙剰鍙鎬ч獙璇?* | 涓嶇‘瀹氬垱鎰忚兘涓嶈兘鎾戣捣闀跨瘒锛岄渶绯荤粺妫€楠?|
| **璁惧畾瑙勮寖鍖?* | 宸叉湁闆舵暎璁惧畾锛岄渶缁撴瀯鍖栥€佸垎灞傚寲銆佹爣鍑嗗寲 |

**涓嶉€傜敤**锛氱煭绡囷紙<10涓囧瓧锛夆啋 鐢?light-bootstrap锛涗粎闇€绋冲畾鎬ф鏌?鈫?鐢?world-stability-check skill銆?

## 杈撳叆琛?

| 杈撳叆椤?| 蹇呴渶 | 璇存槑 | 绀轰緥 |
|--------|:----:|------|------|
| 涔﹀悕 | 鉁?| 浣滃搧姝ｅ紡鍚嶇О | 銆婃繁娓婂綊閫斻€?|
| 鏍稿績鍒涙剰 | 鉁?| 涓€鍙ヨ瘽姒傛嫭 | 涓昏鍦?000灞傛繁娓婁腑瀵绘壘鍥炲鐨勮矾 |
| 骞冲彴 | 鉁?| 鍙戝竷骞冲彴 | qidian / fanqie |
| 瀵规爣涔?| 鉁?| 鑷冲皯1鏈悓绫讳綔鍝?| 銆婅绉樹箣涓汇€?|
| 鏍稿績鐖界偣 | 鉁?| 2-5涓被鍨?| 鎴樺姏鍗囩骇/鏅哄晢纰惧帇 |
| 閲戞墜鎸?| 鍙€?| 涓€鍙ヨ瘽鎻忚堪 | 鏃犻檺澶嶆椿+璁板繂淇濈暀 |

## 鎵ц椤哄簭锛堟寜渚濊禆閾句緷娆℃墽琛岋級

```
Phase 0 (L0鐏甸瓊灞?
    鈫?
Phase 0.3 (鍙傝€冧功鐢勫埆)
    鈫?
Phase 0.4 (閲戞墜鎸囪璁?
    鈫?
Phase 0.5 鈽?(璺ㄥ煙绱犳潗鑱氬悎)  鈫?寮哄埗涓嶅彲璺宠繃
    鈫?
Phase 1 (L1璁惧畾灞傛帹婕?
    鈫?
Phase 1.2 鈽?(L1娣卞害灞曞紑)   鈫?v2.9 閫愮瘒鎵╁啓
    鈫?
Phase 1.3 鈽?(L1浜ゅ弶鍏宠仈)   鈫?v2.9 14瀵瑰叧鑱?
    鈫?
Phase 1.5 (涓栫晫绋冲畾鎬ф楠?
    鈫?
Phase 2 (L2鍗风骇灞曞紑)
    鈫?
Phase 3 (椤圭洰楠ㄦ灦鍒涘缓)
    鈫?
Phase 4 (reader_profile宓屽叆)
    鈫?
Phase 5 (鏁板€间綋绯绘ā鏉垮崌绾?
    鈫?
Phase 6 (瓒呰秺鎬х‖妫€鏌?
```

## Phase 鎸囦护绱㈠紩

褰撳墠澶勪簬绗嚑姝ワ紝灏卞彧鍔犺浇瀵瑰簲鏂囦欢锛?

| Phase | 鏂囦欢 | 绫诲瀷 |
|:------|:-----|:-----|
| Phase 0 | `phases/phase-0.md` | 鐏甸瓊瀵归綈 + PRD + 鍘嬪姏娴嬭瘯 |
| Phase 0.3 | `phases/phase-03.md` | 鍙傝€冧功绛涢€?+ 鎷嗚В + 宸紓鍖?|
| Phase 0.4 | `phases/phase-04.md` | 閲戞墜鎸囪璁?+ 鍥涚骇璇勪及 + 绾︽潫妫€鏌?|
| Phase 0.5 鈽?| `phases/phase-05.md` | 璺ㄥ煙绱犳潗鑱氬悎锛堝己鍒讹級 |
| Phase 1 | `phases/phase-1.md` | L1鍏欢濂楅鏋?|
| Phase 1.2 鈽?| `phases/phase-12.md` | L1娣卞害灞曞紑锛堥€愮瘒鎵╁啓锛?|
| Phase 1.3 鈽?| `phases/phase-13.md` | L1浜ゅ弶鍏宠仈鐭╅樀 |
| Phase 1.5 | `phases/phase-15.md` | 涓栫晫绋冲畾鎬ф楠?|
| Phase 2 | `phases/phase-2.md` | L2鍗风骇灞曞紑 + 鐖界偣璁捐 |
| Phase 3 | `phases/phase-3.md` | 椤圭洰楠ㄦ灦 + 瑙掕壊鍗?+ 鏁版嵁搴?|
| Phase 4 | `phases/phase-4.md` | reader_profile宓屽叆 |
| Phase 5 | `phases/phase-5.md` | 鏁板€间綋绯绘ā鏉?|
| Phase 6 | `phases/phase-6.md` | 瓒呰秺鎬х‖妫€鏌?|

## 璐ㄩ噺鏍囧噯涓庣増鏈?

鍙傝 `references/璐ㄩ噺鏍囧噯.md` | `references/鐗堟湰鍘嗗彶.md` | `references/浜у嚭鐩綍缁撴瀯.md`

<pop-category>bootstrap</pop-category>
<pop-position>1</pop-position>

