---
name: radar-release
description: Validate, merge, deploy, and verify changes to the Startup Product Radar GitHub Pages site using evidence-based release gates. Use whenever implementing or publishing changes in this repository.
---

# Startup Product Radar release skill

Repository: `supplicant-snowstain/startup-product-radar`  
Production: `https://supplicant-snowstain.github.io/startup-product-radar/`  
Deployment workflow: `.github/workflows/pages.yml`

## Default contract

For every feature or fix, work on a dedicated branch and open a pull request. Do not commit feature changes directly to `main`. Treat a user's instruction to continue implementation as authorization to implement and open a PR; **do not assume** it authorizes bypassing test gates. If the user has already authorized auto-merge after validation, follow the guarded release procedure below. Otherwise request merge approval.

## Release gates (all mandatory)

1. **Scope and provenance.** Describe the intended behavior, changed files, and acceptance criteria. Never fabricate product launches, founders, demand, revenue, source URLs, or approved relationship evidence. Keep employer-specific/internal information out of the public repo.
2. **Local/static verification.** Run `python -m unittest discover -s tools/startup_lab/tests -v`, `python tools/test_relationships.py`, `python tools/test_research_feed.py`, and `node --check` on every `web/*.js` when an execution environment is available. Also run applicable feed validators/builders and `startup_lab.check_site` against generated feeds. If execution is unavailable, record this as **not run**; never call it passed.
3. **Pull-request CI.** Wait for every required/applicable GitHub Actions check on the exact PR head SHA to conclude `success`. A queued, in-progress, skipped, missing, or unavailable check is **not a pass**. Check workflow run jobs and failure logs if needed. Do not merge with failing checks, unresolved conflicts, or a changed head SHA.
4. **Merge.** Verify the PR is mergeable, expected head SHA matches, and the user has authorized merge (explicitly or by a standing automation instruction). Prefer squash merge. Record resulting merge commit SHA.
5. **Deploy.** Wait for `Publish Opportunity Explorer` on the **merge commit** to finish successfully, including Pages deployment. A successful merge alone is not a successful deploy. A successful build without the deploy job is not sufficient.
6. **Production acceptance.** Verify the deployed homepage, `graph.html?embed=1`, relevant generated feeds, language switching, node inspection, search/filter behavior, mobile responsiveness, and evidence disclaimers. When a real browser is unavailable, request user confirmation and report browser QA as **unverified**. Verify freshness using a release marker or exact asset/version; don't treat an old cached file as proof of the new release.
7. **Report.** State separate statuses for code, tests, PR, deployment, and production acceptance; include PR URL, commit SHA, failing checks, and next action. Never claim a release is complete until supported by actual evidence.

## Failure and rollback

- On test failure: inspect logs, fix on the feature branch, rerun checks; never force merge.
- On deployment failure: inspect Pages job logs, fix via a new PR; do not claim production success.
- On production regression: assess impact, prepare a revert PR or safe hotfix, and run the same gates. Do not silently rewrite public data.
- If checks take longer than the current interaction: create a bounded follow-up automation **only when authorized**. Monitor the exact PR and head SHA; stop the automation after terminal success or actionable failure. Do not create duplicate monitors for the same PR.

## Useful links

- PRs: https://github.com/supplicant-snowstain/startup-product-radar/pulls
- Actions: https://github.com/supplicant-snowstain/startup-product-radar/actions
- Pages: https://supplicant-snowstain.github.io/startup-product-radar/
