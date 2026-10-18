# CHANGELOG

## v2.0.0 | 2026-10-19

按短剧工作流重排，去掉小说管线的阶段状态机。

- `pop-drama-pipeline` 更名 `pop-drama-workbench`。
- 不再用 phase 1-5，不再强制"立项→舞台→剧情→剧本"。
- 改为模块化路由：market / decon / story / beats / script / review / research 可单独调用。
- 状态文件改为 `00-创作总表.md`，只记项目信息、关键决定、文件索引与进度。
- 新增"导入已有项目"的归位规则与"只提示相关缺口"的原则。

## v1.0.0 | 2026-10-19

首版。短剧剧本线总控，范围到剧本交付与审核。
