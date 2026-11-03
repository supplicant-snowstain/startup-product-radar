# Opportunity Explorer Web Alpha

Static HTML/CSS/JS, no account, API key, or dependency installation.

The displayed signals are generated from `data/provisional/*.json` using:

```bash
PYTHONPATH=tools/startup_lab python -m startup_lab.public_feed --root . --output web/signals.json
```

Use a local HTTP server: `python -m http.server 8000 -d web`, then open http://localhost:8000. Modern browsers block `fetch()` from `file://`, so opening the HTML file directly does not load the data.

The data is explicitly provisional and includes original citations and limitations. Editing data files requires regenerating the feed. The future production workflow must distinguish promotional claims from firsthand user accounts, protect against malicious fields, and preserve links to original source context.

The GitHub Pages workflow publishes the `web/` directory upon pushes to main or manual workflow runs, if Pages deployment is enabled for the repository in GitHub Settings → Pages (GitHub Actions source). Deployment success must be checked in Actions before sharing a live URL.

## Localization

The homepage and exploration detail page support **English (EN), 中文 (zh), français (FR)** via the header selector. The selected language is remembered in localStorage; when no preference is stored, browser language selects the initial locale (fallback EN). UI and signal translations live in `web/locales/en.json`, `web/locales/zh.json`, and `web/locales/fr.json`. `web/i18n.js` loads the JSON resources and controls switching; do not embed source records or private information into the language bundles. The current three provisional records have manually authored presentation summaries in all three languages. Research evidence files, source URLs, original source locators and factual provenance remain unchanged. Future incoming records without a translated summary fall back to the original record text; do not silently claim a machine translation is a sourced statement.

To check: switch locale on homepage, open a card, verify selection persists and questions/limitations switch language; reload; test in mobile width. GitHub Pages deployment and actual end-to-end browser tests still require confirmation.

### Translator workflow

Edit the matching JSON locale file while keeping the same UI keys in every language. Add presentation-only translations for each existing provisional signal in zh/fr, preserving source URLs, provenance, and original statements in `signals.json`. Validate with `PYTHONPATH=tools/startup_lab python -m unittest discover -s tools/startup_lab/tests -v`; CI tests localization key parity and signal coverage. New signals without a translation display original content until translated, not fabricated translations.

## Opportunity Map v0.2

The exploration page displays distinct problem nodes and original-source nodes. Explicit editorial relationships are loaded from `web/opportunity-map.json`; the site **does not** infer that a shared category or shared source establishes the same user need. Edges with `verification: editorial_hypothesis` are labeled provisional. The map is responsive and changes interface language with EN/中文/FR. No claim is made that any link establishes market demand.

**For contributors:** add an edge only when you can state its intended semantic type and specific rationale. Do not add evidence IDs for a relationship until the corresponding evidence genuinely documents that relation. The map is a navigation aid, not an opportunity-scoring algorithm.

## Human-first idea explanations

The first section on each exploration page answers **why someone might build this** through five short steps: a relatable scenario, the friction, a possible product, potential value, and what is still unknown. These are stored in `web/idea-stories.json` in EN/中文/FR. They are **editorial illustrations, not actual founder testimony, customer quotations, or validated demand**. The cited source remains accessible below the story. Avoid attributing invented intentions to creators. For new records, write source-grounded stories and mark assumptions explicitly.

## Product Discovery → Why this product?

Product cards link to `product.html?id=<product-id>`. The page presents a five-step, plain-language idea story (user situation → friction → product approach → possible benefit → uncertainty), original source, and explicitly documented links to problem signals. Optional product stories live in `data/products/*.json` and are included by the `startup_lab.product_feed` generator. No product is created solely to make the interface look populated: an empty feed is displayed honestly until sourced product records exist. Research narratives must never masquerade as verified founder motivations.
