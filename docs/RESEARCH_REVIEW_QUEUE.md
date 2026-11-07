# Research Intelligence Review Queue / 研究审核队列 / File de révision

## 中文

新的日报或产品索引提交到 `main` 后，GitHub Actions 的 **Prepare research intelligence review drafts** 会生成可下载的 `research-intelligence-review-drafts` 构建产物（JSON），保留 30 天。它**不是**网站公开数据，不会修改 `data/research_intelligence.json`，也不会将待审核产品升级为正式新品。

审核流程：

1. 在 [Actions](https://github.com/supplicant-snowstain/startup-product-radar/actions/workflows/research-drafts.yml) 下载最新 JSON；也可以手动运行 `python tools/build_research_drafts.py --root . --output data/research_drafts.json`。
2. 对照 `source_report` 及其中的原始链接逐条核实 `extracted_zh`。自动抽取是启发式的，可能漏掉或错误匹配字段。不得把创始人自述写成独立验证。
3. 补充用户任务、真实工作流、替代方案、正反证据、可证伪实验；完成 zh/en/fr 三语内容。
4. 通过 Pull Request 将审核结果**人工合并**到 `data/research_intelligence.json`。合并后 Pages 构建会在网站详情页展示该产品专属分析。
5. 无法核实的内容留空或明确写 UNKNOWN，不要推断收入、留存、付费或 PMF。观察日期不等于首次发布日期。

数据边界：`index/products.csv` 是既有研究索引，`data/research_intelligence.json` 是已编辑的研究解读（并非商业验证），`data/research_drafts.json` 仅作为本地或 Actions 产物，不能部署。候选目录不会被本工作流读取或发布。

## English

On report or index changes, the **Prepare research intelligence review drafts** workflow uploads a JSON artifact for 30 days. This is **not** a published product feed. Review each excerpt against its original sources, distinguish observed facts from maker claims and inference, add counterevidence and a falsifiable experiment, and provide Chinese/English/French text before manually merging into `data/research_intelligence.json`. Unknown retention, payment and PMF must remain unknown. The workflow never auto-approves products.

## Français

À chaque modification des rapports ou de l'index, le workflow **Prepare research intelligence review drafts** produit un artefact JSON téléchargeable pendant 30 jours. Il ne publie aucun produit. Vérifier chaque extrait auprès des sources, distinguer observations, déclarations et hypothèses, documenter les contre-preuves et les expériences réfutables, puis traduire en chinois, anglais et français avant fusion manuelle dans `data/research_intelligence.json`. Les données inconnues restent inconnues.
