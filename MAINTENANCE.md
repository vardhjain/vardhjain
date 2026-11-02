# Keeping this profile useful

The root README is the public profile. Handwritten project descriptions live outside the `PULSE` markers; the updater changes only the marked block, the two workbench SVGs, and `data/snapshot.json`.

## Refreshing

The **Profile snapshot** workflow validates pull requests without write access. On the default branch it also refreshes after relevant source changes, every day at **09:23 UTC**, or through **Actions → Profile snapshot → Run workflow**. Scheduling begins after the workflow is merged into `main`.

The refresh uses only the built-in `GITHUB_TOKEN`. No personal access token, paid API, third-party stats endpoint, or additional secret is required. Only the refresh job receives `contents: write`; checkout is pinned to a verified commit of `actions/checkout` v6. Nothing runs on `pull_request_target`.

Run locally with Python 3.10+ (standard library only):

```sh
python3 -m unittest discover -s tests -v
python3 scripts/update_profile.py       # fetch public data and regenerate
python3 scripts/update_profile.py --check
python3 scripts/check_profile.py
```

`--check` uses the committed JSON and performs no network requests or writes. `--from-snapshot PATH` regenerates the outputs from a previously fetched snapshot. All source data is fetched and validated before any output is replaced. A network or schema failure fails the job and leaves the previous committed snapshot in place; the visible timestamps reveal its age. A branch protection rule that disallows bot pushes will also fail the refresh without changing the previous snapshot. The workflow never force-pushes.

GitHub may delay scheduled runs, cache images, or disable schedules after 60 days of inactivity in a public repository. Re-enable a disabled workflow under Actions. Bot commits made with `GITHUB_TOKEN` do not recursively trigger this workflow. Concurrent edits can cause a non-fast-forward push failure; rerun the workflow after the other change lands.

## Data definitions

| Field | Source and scope |
| --- | --- |
| Public projects | Paginated `GET /users/vardhjain/repos?type=owner`; public, original, unarchived repositories owned by `vardhjain`, excluding this profile. Forks and private repositories never contribute. This is a repository count, not a count of deployed products. |
| Recent projects | Latest push timestamps of up to three of the four curated projects. A push is not necessarily a release or an individual contribution. |
| MCP tools, tests, coverage | [Published finos-mcp metrics](https://github.com/vardhjain/finos-mcp/blob/metrics/metrics.json). The card includes both fetch time and upstream measurement time. Coverage is rounded to one decimal; failing test count is explicitly shown in the README. |
| Measured commit | The source revision recorded inside the published MCP metrics; linked alongside the card. |

Snapshot JSON stores only these public summaries. It never saves a GitHub token, an email, a phone number, private repository names, or raw API responses.

## Editorial evidence

- **Role, education, workplace impact:** user-supplied resume reviewed November 1, 2026. The 18% abandonment and 30% latency reductions are resume-reported workplace outcomes, not independently audited public benchmarks. The source resume is deliberately not uploaded here because it contains personal contact information. Verify the current role when changing it.
- **FINOS contribution:** [upstream PR #380](https://github.com/finos/ai-governance-framework/pull/380), authored by `vardhjain`, merged October 21, 2026. Its before/after table records 21 restored risk links across eight files. The independent MCP package is not an official FINOS product.
- **EthicLens:** [repository README](https://github.com/vardhjain/Ethiclens) describes Fairlearn parity at 1e-9 and held-out mitigation evaluation. Read its [limitations](https://github.com/vardhjain/Ethiclens/blob/main/LIMITATIONS.md) before making compliance or security claims.
- **GraphRAG:** [reviewer guide](https://github.com/vardhjain/graphrag-pubmedqa-ablation/blob/main/REVIEWER_GUIDE.md) records a historical 37.0% → 59.5% result on 200 questions, a 56.5% majority baseline, historical graph-ingestion concerns, missing raw predictions, and the need for independent replication plus a flat parent-document control. Do not describe the gain as a proven graph advantage or attach these metrics to the hosted demo. Credit is shared with Akash Raghavendra.
- **Secondsight:** [model card](https://github.com/vardhjain/Secondsight/blob/main/docs/MODEL_CARD.md) and [release v0.2.0](https://github.com/vardhjain/Secondsight/releases/tag/v0.2.0). The 93.69% mAP is one historical Market-1501 run with re-ranking, not a multi-seed, cross-dataset, or independently reproduced result. The run periodically monitored the test set; this is disclosed on the profile.
- **Publication link:** taken from the resume; no citation count or publication metric is claimed.

## Design and platform limits

The SVGs are repository-owned, self-contained assets: no JavaScript, external fonts, embedded HTML, tracking pixel, external image dependency, or third-party uptime assumption. Desktop and mobile versions use a `<picture>` element and descriptive fallback text. Header motion is decorative CSS; `prefers-reduced-motion` disables it, and the image is still complete if animation is unavailable.

GitHub sanitizes README HTML and does not execute arbitrary JavaScript. Forms, custom event handlers, live filters, and browser apps belong on a separate website. This profile links existing project tours and demos rather than creating another portfolio to maintain.

Reference: [GitHub profile README requirements](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme), [schedule behavior](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).
