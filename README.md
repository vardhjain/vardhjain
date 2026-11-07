<picture>
  <source media="(max-width: 600px)" srcset="assets/header-mobile.svg">
  <img src="assets/header.svg" alt="Vardh Jain. Machine learning engineer. Build it. Measure it. Make it useful." width="100%">
</picture>

# Hi, I'm Vardh.

I build AI systems that people can question, inspect, and improve. My work spans **agent tooling, retrieval, and responsible ML**—from giving assistants traceable sources to making model evaluations easier to trust.

I'm a **Machine Learning Engineer at MyEdMaster**, working on adaptive tutoring and grounded student assessments. My CS background spans **George Washington University** and **VIT**.

**[LinkedIn ↗](https://www.linkedin.com/in/vardh-jain-258359200/)** &nbsp;·&nbsp; **[Explore my repositories](https://github.com/vardhjain?tab=repositories)** &nbsp;·&nbsp; **[Published research](https://link.springer.com/chapter/10.1007/978-3-031-78931-1_26)**

## A few things I've built

### 01 / Tools that look things up before they answer

**[finos-mcp](https://github.com/vardhjain/finos-mcp)** · Python / MCP / hybrid search

Three read-only MCP servers make financial-industry standards searchable and verifiable: AI governance, the Common Domain Model, and FDC3. Published on PyPI, with offline data, structured validation, and an audit trail. Independent community software, unaffiliated with FINOS.

Building the parsers also surfaced an upstream YAML defect. My **[merged FINOS fix](https://github.com/finos/ai-governance-framework/pull/380)** restored **21 risk links** across eight files.

[Read the engineering story](https://vardhjain.github.io/finos-mcp/) · [Try a real tool call](https://github.com/vardhjain/finos-mcp/blob/main/docs/use-cases.md)

### 02 / From a bias flag to a measured fix

**[EthicLens](https://github.com/vardhjain/Ethiclens)** · FastAPI / React / Postgres / MLflow

A workbench for auditing decision models, comparing mitigations on held-out data, and recording reviewer sign-off. Fairness calculations are checked against Fairlearn to a **1e-9 tolerance**. The emphasis is on measured tradeoffs and clear limits, rather than a claim of legal compliance.

[Try the hosted assistant](https://ethiclens-dun.vercel.app/) · [Explore the methodology](https://vardhjain.github.io/Ethiclens/)

### 03 / Does the graph actually help?

**[GraphRAG / PubMedQA](https://github.com/vardhjain/graphrag-pubmedqa-ablation)** · RAG / knowledge graphs / evaluation

Co-built with [Akash Raghavendra](https://github.com/Akash-Raghavendra). A controlled ablation asks what changes when retrieved fragments expand to their parent abstracts. The historical 200-question run improved accuracy from **37.0% to 59.5%**; it needs a clean replication and a flat parent-document control before attributing the gain to graph structure. The hosted demo is a separate configuration.

[Take the interactive tour](https://graphrag-pubmedqa-ablation.vercel.app/walkthrough) · [Inspect results and caveats](https://github.com/vardhjain/graphrag-pubmedqa-ablation/blob/main/REVIEWER_GUIDE.md)

### 04 / Retrieval across cameras

**[Secondsight](https://github.com/vardhjain/Secondsight)** · PyTorch / ResNet-50 / metric learning

A person re-identification research pipeline with reproducible training, retrieval evaluation, and visual explanations. One historical Market-1501 run reached **93.69% mAP** with re-ranking. The release documents its single-run limits and test-set monitoring history; retrieval rankings are not verified identity decisions.

[See the project tour](https://github.com/vardhjain/Secondsight/blob/main/docs/PROJECT_SHOWCASE.md) · [Inspect the model card](https://github.com/vardhjain/Secondsight/blob/main/docs/MODEL_CARD.md)

## What I bring to a team

At Swankey, I used session analytics and ML to identify setup friction; the targeted fix reduced event-setup abandonment by **18%**. At Virtual Wayback, benchmarking five candidate frameworks helped the team choose a stack and cut prototype latency by **30%**. These are workplace outcomes reported in my resume, separate from the public project benchmarks above.

**My usual toolkit:** Python, SQL, PyTorch, scikit-learn, FastAPI, LangGraph, graph and vector databases, React, Docker, and GitHub Actions.

## The workbench, refreshed daily

<!-- PULSE:START -->
<picture>
  <source media="(max-width: 600px)" srcset="assets/workbench-mobile.svg">
  <img src="assets/workbench.svg" alt="8 public projects; 29 MCP tools; 285 MCP tests passed; 94.9% coverage. Snapshot 2026-11-07." width="100%">
</picture>

**Recently updated projects** (latest repository push, not a new release):

- [finos-mcp](https://github.com/vardhjain/finos-mcp) · 2026-11-06
- [Secondsight](https://github.com/vardhjain/Secondsight) · 2026-11-02
- [Ethiclens](https://github.com/vardhjain/Ethiclens) · 2026-10-27

[Snapshot data](data/snapshot.json) · [MCP metric source](https://github.com/vardhjain/finos-mcp/blob/metrics/metrics.json) · [Measured commit](https://github.com/vardhjain/finos-mcp/commit/93e95163296b13f37ed62b1e20f1ec9c92ad6cf2)
  
MCP run: 2026-11-06; 0 failing tests in that snapshot. Project count excludes forks, archived repositories, and this profile.
<!-- PULSE:END -->

<details>
<summary>How this profile stays current</summary>

The header is a lightweight SVG animation with a reduced-motion fallback. GitHub READMEs don't execute arbitrary JavaScript, so a scheduled GitHub Action fetches public repository metadata and published MCP metrics, then commits the updated SVGs and this snapshot. No third-party stats service or personal access token is needed.

The timestamps show when data was fetched and when the upstream benchmark ran. If an update fails, the last successful snapshot stays visible. GitHub may cache images or delay scheduled runs; schedules can be disabled after 60 days of repository inactivity.

See [maintenance notes](MAINTENANCE.md) for sources, update instructions, and limitations.

</details>

---

**Have a problem where the evaluation matters as much as the demo? [Let's connect.](https://www.linkedin.com/in/vardh-jain-258359200/)**
