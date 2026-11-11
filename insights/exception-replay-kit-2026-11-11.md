# 2026-11-11｜从 Agent 执行到可复现的例外证据

观察日：2026-11-11（Europe/Paris）。证据层级：产品发布页为 OBSERVED（存在该声明），功能效果仍为 CLAIMED；需求关联为 INFERRED。

## 三个需求信号

1. **例外处理**：会计自动化 [Latch](https://www.producthunt.com/products/latch-ai-2) 与探索式 QA [Seldon](https://www.producthunt.com/products/seldon) 均强调非标准路径。尚未证实独立用户需求强度。
2. **解释与回放**：[Co-Review](https://www.producthunt.com/products/co-review) 追问生成代码原因，Seldon 回放失败路径，Latch 留执行日志。与 [2026-11-10 Agent Evidence Receipt](agent-evidence-receipt-2026-11-10.md) 假设相关，但不能推导出 PMF。
3. **不依赖 AI 的细分价值**：[Opal Reader](https://www.producthunt.com/products/opal-reader) 的折叠屏阅读笔记布局与 [Ember](https://www.producthunt.com/products/ember-117) 的自托管聊天，表明交互/成本/控制权也能成为差异化。

## 独立产品假设：Exception Replay Kit

目标：5–20 人的小型 Web QA/自动化团队。MVP：Playwright 脱敏执行轨迹 + 截图 + 失败步骤，输出可分享的本地 HTML 报告。先不用 LLM；对照 Playwright Trace Viewer、CI artifacts 和传统录屏。2 周内访谈 8 人，试用 5 支团队。成功：≥4/8 人有最近 30 天真实痛点，≥3/5 团队复用，中位定位时间减少 ≥30%，无敏感信息泄漏；失败：<2/5 复用或复现错误率 >20% 或任何泄漏。均为**未来实验阈值**，不是既有数据。

## 反证与未决

Playwright Trace Viewer 已支持大量调试需求；额外产品可能仅增加维护负担。公开榜单评论与排名不等于实际客户、留存或付费。融资/创业者真实转向历史未知。下一轮优先找用户公开抱怨、失败项目及能复核的原始访谈。

主报告：[2026-11-11](../reports/2026/11/2026-11-11.md)。
