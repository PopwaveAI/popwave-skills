# Step 6：质量门禁

**读什么：** Step 5 产出的完整 HTML。

**标准检查清单：**
```
[ ] CSS 变量名全部来自 DESIGN_CORE（不自行发明）
[ ] 至少使用了 3 种组件库中的组件
[ ] 组件 class 名与 components.md 一致
[ ] 响应式三断点已支持
[ ] 双击 HTML 可直接在浏览器打开（零外部依赖）
[ ] 零 emoji（所有视觉标识用 CSS/SVG 实现）
[ ] 没有 <style> @import — 全部内联
[ ] 没有 <script src="..."> 外部库 — 全部内联（Chart.js CDN 除外）
[ ] Chart.js 统一使用 CDN 引用 v4.4.0

<!-- 反模式检查 -->
[ ] 没有 `body { overflow-x: hidden; }`（用 html { overflow-x: clip; }）
[ ] 没有纯色/渐变色块代替配图
[ ] 阅读器中 text-indent 生效（段内\n 未转<br>）
[ ] CSS 中同一颜色值没有在 3 个以上地方硬编码
```

**门禁：** 标准检查任一项不通过 → **退回** 修改。配图铁律任一项不通过 → 整次不合格。

**产出：** 验证通过的最终 HTML。
