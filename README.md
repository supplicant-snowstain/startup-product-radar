# ✳ Startup Product Radar

**中文 · [English](#english) · [Français](#français)**

<!-- DAILY_RADAR_START -->
## 🛰️ Latest research / 最新研究 / Dernières recherches

**Latest: 2026-11-08 (Europe/Paris)** · [中文深度报告](reports/2026/11/2026-11-08.md) · [All reports / 全部日报](reports/README.md)

> **研究提醒：** 本栏目按报告观察日期排列，**不代表产品首次发布日期**。产品榜单、创始人主张和融资不等于留存或 PMF；请阅读报告中的原始证据与反面证据。

| Date (Paris) | Featured research (observed products) | Full report |
| --- | --- | --- |
| 2026-11-08 | Research report (see evidence and limitations) | [Read](reports/2026/11/2026-11-08.md) |
| 2026-11-07 | Glasshand · Maritime | [Read](reports/2026/11/2026-11-07.md) |
| 2026-11-06 | Pushary for Teams · Okapi · Tao Browser · Pinku · … | [Read](reports/2026/11/2026-11-06.md) |
| 2026-11-05 | Chromagraph Camera · Tiny Computers · HackerTV · Synkr | [Read](reports/2026/11/2026-11-05.md) |
| 2026-11-04 | AgentKit by Scalekit · Testifly | [Read](reports/2026/11/2026-11-04.md) |

**Browse:** [Product profiles / 产品档案](products/) · [Insights / 需求洞察](insights/) · [Structured index / 产品索引](index/products.csv) · [Methodology / 研究方法](METHODOLOGY.md)

*Reports are public research; staged product candidates are **not** automatically published as verified launches.*

<!-- DAILY_RADAR_END -->

**[🌐 Open interactive demo / 打开交互演示 / Ouvrir la démo](https://supplicant-snowstain.github.io/startup-product-radar/)**

> **Deployment status / 部署状态 / État du déploiement:** Website URL is the configured GitHub Pages destination; successful publication has **not yet been independently confirmed**. Check [Actions / 部署记录 / Exécutions](https://github.com/supplicant-snowstain/startup-product-radar/actions/workflows/pages.yml). If unavailable, see local instructions below.

![Alpha](https://img.shields.io/badge/status-alpha-c4e86e) ![License](https://img.shields.io/badge/license-not%20yet%20specified-lightgrey)

---

<a id="中文"></a>
## 中文

### 不要从点子开始，从一个问题开始。

Startup Product Radar 是面向独立开发者的开源创业机会探索工具。它从公开用户反馈和产品信息中整理**可追溯的问题线索**，帮助你发现值得进一步研究的方向，而不是预测下一个成功创业项目。

**[进入交互网页](https://supplicant-snowstain.github.io/startup-product-radar/)** · [查看网页源码](web/) · [研究方法](METHODOLOGY.md) · [路线图](docs/CURRENT_FOCUS.md)

**每日研究展示：** 交互网站已加入独立的 Daily Research 区域；Pages 构建时从 `reports/` 和 `index/products.csv` 生成 `web/research.json`，展示最近研究报告与观察产品，**不将待审核候选视为正式新品**。是否已部署成功仍需检查 [GitHub Actions](https://github.com/supplicant-snowstain/startup-product-radar/actions/workflows/pages.yml)。

**新增 Product Discovery：** 网站已加入新产品区域与产品数据接口，但目前已收录 3 个有官方开源来源的产品案例（uv、Immich、Memos），但它们不是今日新品；网页现已将「有日期证据的新品」和「产品创意案例」分开显示。每日研究任务的结果还没有经过验证的自动入库链路，不应理解为已经每天更新网站。

**现在能做什么？** 浏览并搜索公开问题线索；点击卡片进入独立探索页；查看原始来源、证据局限和待研究问题；通过 Opportunity Map 探索明确标注的相关关系。网页支持中文、英文、法文切换。

**本地运行**：克隆仓库后，在仓库根目录运行：

```bash
python -m http.server 8000 -d web
```

随后访问 `http://localhost:8000`。网页通过 HTTP 读取 JSON 数据，直接双击 HTML 文件可能无法加载数据。

**证据说明：** 目前公开数据仅有少量待复核的来源线索。用户评论、创始人表述、关联假设并不等于经过验证的市场需求，也不能据此宣称产品市场匹配。

---

<a id="english"></a>
## English

### Don't start with an idea. Start with a problem.

Startup Product Radar is an open-source opportunity exploration workbench for independent builders. It collects **traceable public problem signals** and helps you investigate user friction, existing solutions, and unanswered questions — without predicting startup success.

**[Launch interactive demo](https://supplicant-snowstain.github.io/startup-product-radar/)** · [Web source](web/) · [Research methodology](METHODOLOGY.md) · [Roadmap](docs/CURRENT_FOCUS.md)

**Daily Research:** The site has a separate research section generated from dated reports and the existing product index at Pages build time. Research observations are not verified launches. Deployment remains unconfirmed until Actions succeeds.

**Product Discovery:** A new-product panel and publishing feed have been added. The initial catalog now includes three sourced existing-product case studies (uv, Immich, Memos); these are not newly launched today. The website now separates dated launches from idea case studies; the scheduled daily report has not yet been confirmed to automatically populate the website.

**What can you do?** Browse and search provisional signals, open evidence-backed exploration pages, inspect source links and limitations, and navigate explicitly labeled hypotheses in the Opportunity Map. The website offers Chinese, English, and French.

**Run locally:** Clone the repository, then from the repository root:

```bash
python -m http.server 8000 -d web
```

Open `http://localhost:8000`. A local HTTP server is required to fetch JSON data; double-clicking the HTML file may not work.

**Evidence notice:** The initial dataset contains only a few provisional signals. Public anecdotes, founder claims, and proposed links are **not independently validated customer demand**.

---

<a id="français"></a>
## Français

### Ne partez pas d'une idée. Partez d'un problème.

Startup Product Radar est un outil open source d'exploration d'opportunités destiné aux créateurs indépendants. Il rassemble des **signaux publics traçables** afin d'examiner les difficultés des utilisateurs, les solutions existantes et les questions encore ouvertes, sans prétendre prédire le succès d'une entreprise.

**[Ouvrir la démo interactive](https://supplicant-snowstain.github.io/startup-product-radar/)** · [Code du site](web/) · [Méthodologie](METHODOLOGY.md) · [Feuille de route](docs/CURRENT_FOCUS.md)

**Veille quotidienne :** Le site propose une section de rapports de recherche générée lors du déploiement. Les observations ne sont pas des lancements vérifiés. Le déploiement reste à confirmer dans Actions.

**Découverte de produits :** Un espace dédié et un flux de données sont disponibles, mais trois fiches de produits existants (uv, Immich, Memos) sont maintenant publiées ; ce ne sont pas des lancements du jour. Le site distingue les lancements datés des études de cas. La mise à jour automatique depuis la veille quotidienne n'est pas encore validée.

**Fonctions actuelles :** recherche de signaux provisoires, pages d'exploration avec sources et limites, et carte des relations explicitement présentées comme des hypothèses. Le site propose le chinois, l'anglais et le français.

**Exécution locale :** Clonez le dépôt puis lancez, depuis sa racine :

```bash
python -m http.server 8000 -d web
```

Ouvrez `http://localhost:8000`. Le serveur HTTP local permet le chargement des fichiers JSON, ce qui peut échouer lors de l'ouverture directe du fichier HTML.

**Précaution :** Les premiers signaux restent à vérifier. Des témoignages isolés, des déclarations de fondateurs ou des liens hypothétiques ne constituent pas une demande de marché validée.

---

## Project / 项目资料 / Ressources

[Research reports / 每日报告 / Rapports](reports/README.md) · [Public evidence / 公开证据 / Preuves](data/provisional/README.md) · [Web documentation](web/README.md) · [Release criteria](docs/FIRST_USABLE_RELEASE.md) · [GitHub Actions](https://github.com/supplicant-snowstain/startup-product-radar/actions)

**Contributing / 参与贡献 / Contribuer:** Corrections, accessibility improvements, translations, and well-sourced public observations are welcome. Do not upload confidential employer material, credentials, private personal information, or invented user testimony.

**Publishing:** The GitHub Pages workflow builds and tests the site. An automated workflow configuration is not proof of a successful deployment; check the Actions run before treating the URL as live.
