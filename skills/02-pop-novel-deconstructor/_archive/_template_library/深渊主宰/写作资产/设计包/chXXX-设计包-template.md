# Template: 章级设计包
# @consumed_by: pop-novel-prose-render Step 1~3

scene:
  type: ""
  location: ""
  time: ""
  word_count: 2500

battle_formula:
  phases:
    - "战前准备: avg2段 — 环境感知/敌人定位/武器检查"
    - "对峙: avg3段 — 语言威胁+心理博弈"
    - "攻防交替: avg6段 — 来回3-4轮"
    - "转折: avg2段 — 对手破绽"
    - "终击: avg3段 — 一击致命(割喉)"
    - "战后处理: avg2段 — 搜刮+转移"
  sensory_mix: {visual:50, auditory:15, tactile:25, emotional:10}
  fatigue_management: {max_consecutive_battle:2, cooldown:1, cooldown_type:"升级/日常"}

chapter_structure:
  avg_paragraphs: 35
  avg_scenes: 4
  scene_transition: "空间跳(直接切黑)"
  paragraph_pattern: "长短交替(战斗短句密集/日常长句)"

info_density:
  per_chapter: {event_count:5, dialogue_ratio:35, description_ratio:30, inner_monologue_ratio:15, combat_ratio:20}

render_strategy:
  pov_switch: "固定视角(索伦) + 偶尔切薇薇安"
  narrator_distance: "近(贴主角脑内) - 战斗时中距"
  timeline: "纯顺序"

climax_construction: {buildup:3, climax_paragraphs:12, cooldown:1, ratio:"3:1"}
