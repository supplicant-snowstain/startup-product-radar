# Research Intelligence Review Queue / 研究审核队列 / File de révision

## 中文

新的日报或产品索引提交到 `main` 后，GitHub Actions 的 **Prepare research intelligence review drafts** 会生成可下载的 `research-intelligence-review-drafts` 构建产物（JSON），保留 30 天。它**不是**网站公开数据，不会修改 `data/research_intelligence.json`，也不会将待审核产品升级为正式新品。

可视化审核工作台：<https://supplicant-snowstain.github.io/startup-product-radar/review.html>。在浏览器中导入 Actions 下载的 JSON，逐产品编辑中英法字段，检查完整性并导出单产品审核文件。所有编辑仅在当前浏览器页面内，刷新会丢失；不上传到服务器。导出内容仍须人工核查并合并进正式知识库。\n\n审核流程：

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

## Review export → Pull Request / 审核文件提交 PR / Export vers PR

1. 在 `review.html` 完成所有语言字段并下载 `<slug>-reviewed.json`。此文件仍标记为 `requires_maintainer_approval`，不是已验证事实。
2. 在本地仓库中运行：

   ```bash
   python tools/prepare_research_review.py --root . --review path/to/<slug>-reviewed.json --output /tmp/research_intelligence_candidate.json
   ```

   工具会检查产品是否在索引中、原始日报是否存在、三语字段是否齐全、是否存在重复条目，并拒绝直接覆盖正式知识库。
3. 人工比较生成的候选 JSON 与 `data/research_intelligence.json`，核对证据后在单独分支将经过审核的新条目合并进该文件，提交 Pull Request。**不要把整个候选 JSON 直接覆盖可能已被其他贡献者更新的正式文件。**
4. `Validate research intelligence review` 将在 PR 上运行校验；维护者审查原始证据后再合并。GitHub Pages 只在合并到 main 后发布。

**Limitations:** 当前尚不支持从静态网站直接创建 PR；不要求用户提供 GitHub token 给网页。CI 只检查结构与来源文件关联，不能自动证明引用真实性、译文准确性、商业指标或产品市场匹配。

**English:** Export a reviewed item, run the validation/preparation CLI, inspect the diff and submit a PR on a separate branch. CI checks structure, not factual truth. No browser token or automatic merge.

**Français :** Exporter la fiche, exécuter le validateur, contrôler les différences et soumettre une PR depuis une branche dédiée. Les tests vérifient la structure, pas la véracité des affirmations.
