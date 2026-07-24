<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{PROJECT_NAME}} · 项目状态</title>
<style>
  :root {
    --bg: #0f1117;
    --card-bg: #1a1d27;
    --card-border: #2a2d3a;
    --text: #e4e6eb;
    --text-dim: #8b8fa3;
    --accent: #6c5ce7;
    --accent-light: #a29bfe;
    --green: #00b894;
    --red: #e17055;
    --yellow: #fdcb6e;
    --gray: #636e72;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 24px;
  }
  .container { max-width: 960px; margin: 0 auto; }

  /* Header */
  .header {
    background: linear-gradient(135deg, var(--accent), var(--accent-light));
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 24px;
  }
  .header h1 { font-size: 24px; font-weight: 700; margin-bottom: 8px; }
  .header .meta { font-size: 13px; opacity: 0.85; display: flex; gap: 20px; flex-wrap: wrap; }
  .header .meta span { display: flex; align-items: center; gap: 4px; }
  .header .phase-badge {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    margin-top: 8px;
  }

  /* Phase Progress */
  .phase-progress {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 24px;
  }
  .phase-progress h2 { font-size: 16px; margin-bottom: 18px; color: var(--text-dim); }
  .phase-timeline {
    display: flex;
    align-items: center;
    gap: 0;
    overflow-x: auto;
    padding-bottom: 4px;
  }
  .phase-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    min-width: 100px;
    position: relative;
  }
  .phase-circle {
    width: 36px; height: 36px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
    border: 2px solid var(--card-border);
    background: var(--bg);
    z-index: 1;
  }
  .phase-circle.done { background: var(--green); border-color: var(--green); }
  .phase-circle.current { background: var(--accent); border-color: var(--accent-light); box-shadow: 0 0 12px rgba(108,92,231,0.5); }
  .phase-circle.pending { background: var(--bg); border-color: var(--gray); }
  .phase-line {
    flex: 1; height: 3px; min-width: 20px;
    background: var(--card-border);
    margin-top: -22px;
  }
  .phase-line.done { background: var(--green); }
  .phase-label { font-size: 11px; color: var(--text-dim); text-align: center; line-height: 1.3; }
  .phase-label.active { color: var(--accent-light); font-weight: 600; }

  /* Cards Row */
  .cards-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; }
  @media (max-width: 700px) { .cards-row { grid-template-columns: 1fr; } }

  .card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 24px;
  }
  .card h2 { font-size: 15px; color: var(--text-dim); margin-bottom: 16px; }

  /* Deck Cards */
  .deck-item {
    display: flex; align-items: center; justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid var(--card-border);
    font-size: 14px;
  }
  .deck-item:last-child { border-bottom: none; }
  .deck-item .name { display: flex; align-items: center; gap: 8px; }
  .deck-item .path { font-size: 12px; color: var(--text-dim); }
  .deck-status {
    padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 600;
  }
  .deck-status.ready { background: rgba(0,184,148,0.15); color: var(--green); }
  .deck-status.not-ready { background: rgba(225,112,85,0.15); color: var(--red); }
  .deck-status.skipped { background: rgba(99,110,114,0.15); color: var(--gray); }

  /* Creative Summary */
  .summary-item { margin-bottom: 12px; }
  .summary-item .label { font-size: 12px; color: var(--text-dim); margin-bottom: 4px; }
  .summary-item .value { font-size: 15px; }

  /* Recent Outputs */
  .outputs-table { width: 100%; border-collapse: collapse; font-size: 14px; }
  .outputs-table th {
    text-align: left; padding: 10px 12px;
    color: var(--text-dim); font-size: 12px; font-weight: 600;
    border-bottom: 1px solid var(--card-border);
  }
  .outputs-table td {
    padding: 10px 12px;
    border-bottom: 1px solid var(--card-border);
  }
  .outputs-table tr:last-child td { border-bottom: none; }
  .outputs-table .file-path { font-family: 'Consolas', 'Courier New', monospace; font-size: 13px; color: var(--accent-light); }

  /* Next Step */
  .next-step {
    background: linear-gradient(135deg, rgba(108,92,231,0.15), rgba(162,155,254,0.08));
    border: 1px solid var(--accent);
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 24px;
  }
  .next-step h2 { font-size: 14px; color: var(--accent-light); margin-bottom: 8px; }
  .next-step .action { font-size: 15px; }
  .next-step .prereq { font-size: 13px; color: var(--text-dim); margin-top: 8px; }

  /* Chapter Badge */
  .chapter-badge {
    display: inline-block;
    background: var(--accent);
    color: white;
    padding: 4px 12px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    font-family: 'Consolas', 'Courier New', monospace;
  }

  /* Footer */
  .footer { text-align: center; font-size: 12px; color: var(--text-dim); padding: 16px 0; }
</style>
</head>
<body>
<div class="container">

  <!-- Header -->
  <div class="header">
    <h1>{{PROJECT_NAME}}</h1>
    <div class="meta">
      <span>管线：番茄skill群</span>
      <span>创建：{{CREATED_AT}}</span>
      <span>更新：{{UPDATED_AT}}</span>
    </div>
    <div class="phase-badge">模式：{{MODE}} · 当前阶段：{{PHASE}} · {{CURRENT_CHAPTER}}</div>
  </div>

  <!-- Phase Progress -->
  <div class="phase-progress">
    <h2>Phase 进度</h2>
    <div class="phase-timeline">
      {{PHASE_CHECKLIST}}
    </div>
  </div>

  <!-- Next Step -->
  <div class="next-step">
    <h2>下一步操作</h2>
    <div class="action">{{NEXT_STEP}}</div>
  </div>

  <!-- Cards Row -->
  <div class="cards-row">
    <!-- Deck Readiness -->
    <div class="card">
      <h2>底牌就绪</h2>
      {{DECK_CARDS}}
    </div>

    <!-- Creative Summary -->
    <div class="card">
      <h2>创意摘要</h2>
      {{CREATIVE_SUMMARY}}
    </div>
  </div>

  <!-- Recent Outputs -->
  <div class="card" style="margin-bottom:24px;">
    <h2>最近产出</h2>
    <table class="outputs-table">
      <thead>
        <tr><th>阶段</th><th>产出文件</th><th>落盘时间</th></tr>
      </thead>
      <tbody>
        {{RECENT_OUTPUTS}}
      </tbody>
    </table>
  </div>

  <!-- Footer -->
  <div class="footer">
    pop-fanqie-pipeline v3.0.0 · project-state.html · 自动生成，请勿手动编辑
  </div>

</div>
</body>
</html>
