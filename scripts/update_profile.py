#!/usr/bin/env python3
"""Refresh public-only profile data. Python standard library; no paid APIs."""

import argparse
from datetime import datetime, timezone
from html import escape
import json
import math
import os
from pathlib import Path
import re
import tempfile
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OWNER = "vardhjain"
FEATURED = {"finos-mcp", "Ethiclens", "graphrag-pubmedqa-ablation", "Secondsight"}
START, END = "<!-- PULSE:START -->", "<!-- PULSE:END -->"


def get_json(url):
    headers = {"User-Agent": "vardhjain-profile", "Accept": "application/json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(url, headers=headers), timeout=30) as response:
        return json.load(response)


def timestamp(value):
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("Source timestamp needs a timezone")
    return result.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def number(value, label, *, maximum=None, integer=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"Invalid {label}")
    if not math.isfinite(value) or value < 0 or (maximum is not None and value > maximum):
        raise ValueError(f"Out-of-range {label}")
    if integer and not isinstance(value, int):
        raise ValueError(f"Non-integer {label}")
    return value


def collect():
    public = []
    for page in range(1, 11):
        # The public user endpoint is deliberate: never enumerate private repositories.
        batch = get_json(
            f"https://api.github.com/users/{OWNER}/repos?type=owner&per_page=100&page={page}"
        )
        if not isinstance(batch, list):
            raise ValueError("Expected a public repository list")
        public.extend(batch)
        if len(batch) < 100:
            break
    else:
        raise ValueError("Repository pagination limit exceeded; do not publish a partial count")

    projects = [r for r in public if not r.get("private", True)
                and r.get("visibility", "public") == "public"
                and r["owner"]["login"].lower() == OWNER
                and not r.get("fork", True) and not r.get("archived", True)
                and r["name"] != OWNER]
    if len({r["name"] for r in projects}) != len(projects):
        raise ValueError("Duplicate repositories in paginated response")
    recent = sorted((r for r in projects if r["name"] in FEATURED),
                    key=lambda r: timestamp(r["pushed_at"]), reverse=True)[:3]
    if len(recent) != 3:
        raise ValueError("Expected at least three public featured projects")

    metrics = get_json(f"https://raw.githubusercontent.com/{OWNER}/finos-mcp/metrics/metrics.json")
    tests = metrics["tests"]
    snapshot = {
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "public_projects": len(projects),
        "recent": [{"name": r["name"], "pushed_at": timestamp(r["pushed_at"])} for r in recent],
        "mcp": {
            "commit": metrics["commit"], "measured_at": timestamp(metrics["generated_at"]),
            "tools": metrics["exposure"]["tools_total"],
            "tests_passed": tests["passed"], "tests_failed": tests["failed"],
            "coverage_pct": tests["coverage_pct"],
        },
    }
    validate(snapshot)
    return snapshot


def validate(data):
    timestamp(data["fetched_at"])
    number(data["public_projects"], "project count", integer=True)
    mcp = data["mcp"]
    if not re.fullmatch(r"[0-9a-f]{40}", mcp["commit"]):
        raise ValueError("Invalid source commit")
    timestamp(mcp["measured_at"])
    for key in ("tools", "tests_passed", "tests_failed"):
        number(mcp[key], key, integer=True)
    number(mcp["coverage_pct"], "coverage", maximum=100)
    if len(data["recent"]) > 3:
        raise ValueError("Too many recent projects")
    for repo in data["recent"]:
        if repo["name"] not in FEATURED:
            raise ValueError("Recent repository is not in the curated public set")
        timestamp(repo["pushed_at"])


def text(x, y, value, size=14, color="#a7bbcf", extra=""):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" {extra}>{escape(str(value))}</text>'


def render_card(data, mobile=False):
    mcp = data["mcp"]
    width, height = (440, 350) if mobile else (900, 230)
    cells = [(str(data["public_projects"]), "PUBLIC PROJECTS"),
             (str(mcp["tools"]), "AI-CALLABLE TOOLS"),
             (str(mcp["tests_passed"]), "MCP TESTS PASSED"),
             (f'{mcp["coverage_pct"]:.1f}%', "MCP COVERAGE")]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
             f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
             '<title id="title">Public workbench snapshot</title>',
             f'<desc id="desc">{escape("; ".join(f"{v} {label.lower()}" for v, label in cells))}. '
             f'Fetched {escape(data["fetched_at"])}. MCP metrics measured {escape(mcp["measured_at"])}. '
             f'{mcp["tests_failed"]} failing MCP tests in source snapshot.</desc>',
             '<style>text{font-family:Arial,Helvetica,sans-serif}.label{font-family:Consolas,monospace;letter-spacing:1px}</style>',
             f'<rect width="{width}" height="{height}" rx="18" fill="#101c2c"/>',
             f'<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="18" fill="none" stroke="#2b3d51"/>',
             '<circle cx="29" cy="31" r="4" fill="#67e8c4"/>',
             text(43, 35, "PUBLIC WORK / LATEST SNAPSHOT", 11, "#c3d4e5", 'class="label"')]
    for index, (value, label) in enumerate(cells):
        x = 26 + (index % 2) * 208 if mobile else 28 + index * 219
        y = 100 + (index // 2) * 100 if mobile else 108
        parts += [text(x, y, value, 35 if mobile else 38, "#67e8c4", 'font-weight="700"'),
                  text(x, y + 25, label, 10, "#c3d4e5", 'class="label"')]
        if index == 1:
            parts.append(text(x, y + 43, "ACROSS 3 MCP SERVERS", 9, "#819bb3", 'class="label"'))
    line_y = 242 if mobile else 158
    parts.append(f'<path d="M26 {line_y}H{width-26}" stroke="#2b3d51"/>')
    fetched = data["fetched_at"].replace("T", " ").replace("Z", " UTC")
    measured = mcp["measured_at"].replace("T", " ").replace("Z", " UTC")
    parts += [text(26, line_y + 27, f"Fetched {fetched}", 11),
              text(26, line_y + 47, f"MCP run {measured}", 11)]
    if mobile:
        parts.append(text(26, line_y + 77, "PUBLIC DATA. TRACEABLE SOURCES.", 10, "#819bb3", 'class="label"'))
    else:
        parts.append(text(617, line_y + 47, "PUBLIC DATA. TRACEABLE SOURCES.", 10, "#819bb3", 'class="label"'))
    return "\n".join(parts) + "\n</svg>\n"


def render_section(data):
    m = data["mcp"]
    alt = (f'{data["public_projects"]} public projects; {m["tools"]} AI-callable tools across 3 MCP servers; '
           f'{m["tests_passed"]} MCP tests passed; {m["coverage_pct"]:.1f}% coverage. '
           f'Snapshot {data["fetched_at"][:10]}.')
    lines = [START, '<picture>',
             '  <source media="(max-width: 600px)" srcset="assets/workbench-mobile.svg">',
             f'  <img src="assets/workbench.svg" alt="{escape(alt, quote=True)}" width="100%">',
             '</picture>', '',
             f'finos-mcp exposes **{m["tools"]} AI-callable tools across 3 MCP servers**. '
             'These are functions an AI assistant can call to look up a governance control, '
             'validate a trade document, or find an FDC3 action.', '',
             '**Recently updated projects** (by latest repository push):', '']
    for repo in data["recent"]:
        lines.append(f'- [{repo["name"]}](https://github.com/{OWNER}/{repo["name"]}) · {repo["pushed_at"][:10]}')
    lines += ['', f'[Snapshot data](data/snapshot.json) · '
              f'[MCP metric source](https://github.com/{OWNER}/finos-mcp/blob/metrics/metrics.json) · '
              f'[Measured commit](https://github.com/{OWNER}/finos-mcp/commit/{m["commit"]})',
              f'  \nMCP run: {m["measured_at"][:10]}; {m["tests_failed"]} failing tests in that snapshot. '
              'Project count excludes forks, archived repositories, and this profile.', END]
    return "\n".join(lines)


def replace_section(readme, section):
    if readme.count(START) != 1 or readme.count(END) != 1 or readme.index(START) >= readme.index(END):
        raise ValueError("README must have exactly one correctly ordered snapshot marker pair")
    before, rest = readme.split(START)
    _, after = rest.split(END)
    return before + section + after


def outputs(data, readme):
    # Fully validate and render before touching any files, so failures preserve the old snapshot.
    validate(data)
    return {
        "README.md": replace_section(readme, render_section(data)),
        "assets/workbench.svg": render_card(data),
        "assets/workbench-mobile.svg": render_card(data, mobile=True),
        "data/snapshot.json": json.dumps(data, indent=2, sort_keys=True) + "\n",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check committed output, without network or writes")
    parser.add_argument("--from-snapshot", type=Path, help="Render a previously fetched public snapshot")
    args = parser.parse_args()
    if args.check and args.from_snapshot:
        parser.error("--check cannot be combined with --from-snapshot")
    if args.check:
        data = json.loads((ROOT / "data/snapshot.json").read_text(encoding="utf-8"))
    elif args.from_snapshot:
        data = json.loads(args.from_snapshot.read_text(encoding="utf-8"))
    else:
        data = collect()
    rendered = outputs(data, (ROOT / "README.md").read_text(encoding="utf-8"))
    if args.check:
        changed = [name for name, content in rendered.items()
                   if not (ROOT / name).exists() or (ROOT / name).read_text(encoding="utf-8") != content]
        if changed:
            raise SystemExit("Snapshot outputs out of sync: " + ", ".join(changed))
        print("Committed snapshot and SVGs are consistent.")
        return
    for name, content in rendered.items():
        dest = ROOT / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="\n", dir=dest.parent, delete=False) as temp:
            temp.write(content)
        os.replace(temp.name, dest)
    print("Updated public profile snapshot.")


if __name__ == "__main__":
    main()
