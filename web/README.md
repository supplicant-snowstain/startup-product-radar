# Opportunity Explorer Web Alpha

Static HTML/CSS/JS, no account, API key, or dependency installation.

The displayed signals are generated from `data/provisional/*.json` using:

```bash
PYTHONPATH=tools/startup_lab python -m startup_lab.public_feed --root . --output web/signals.json
```

Open `web/index.html` directly to view the checked-in feed. A local HTTP server also works (`python -m http.server 8000 -d web`).

The data is explicitly provisional and includes original citations and limitations. Editing data files requires regenerating the feed. The future production workflow must distinguish promotional claims from firsthand user accounts, protect against malicious fields, and preserve links to original source context.

The GitHub Pages workflow publishes the `web/` directory upon pushes to main or manual workflow runs, if Pages deployment is enabled for the repository in GitHub Settings → Pages (GitHub Actions source). Deployment success must be checked in Actions before sharing a live URL.
