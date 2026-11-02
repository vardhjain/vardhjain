#!/usr/bin/env python3
"""Offline checks for profile links, SVG safety, and accidental contact details."""

from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def main():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    links = re.findall(r'\]\(([^\s)]+)\)|(?:src|srcset)="([^"]+)"', readme)
    for pair in links:
        link = next(part for part in pair if part)
        parsed = urlsplit(link)
        if parsed.scheme:
            assert parsed.scheme == "https", f"Unexpected link scheme: {link}"
            continue
        if not parsed.path:
            continue
        target = (ROOT / unquote(parsed.path)).resolve()
        assert target.is_relative_to(ROOT), f"Link escapes repository: {link}"
        assert target.is_file(), f"Broken local link: {link}"
    assert not re.search(r"mailto:|tel:|\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b", readme), "Contact detail in README"
    assert not re.search(r"\+?1[ (.-]+202[ ).-]+867[ .-]+5902", readme), "Phone number in README"
    for path in (ROOT / "assets").glob("*.svg"):
        svg = ET.fromstring(path.read_text(encoding="utf-8"))
        ns = {"s": "http://www.w3.org/2000/svg"}
        assert svg.find("s:title", ns) is not None, f"Missing SVG title: {path}"
        assert svg.find("s:desc", ns) is not None, f"Missing SVG description: {path}"
        for element in svg.iter():
            tag = element.tag.rsplit("}", 1)[-1]
            assert tag not in {"script", "foreignObject", "image", "a"}, f"Active/external SVG content: {path}"
            assert not any(key.lower().startswith("on") or key.endswith("href") for key in element.attrib), path
    print(f"Checked {len(links)} README links/assets and four self-contained SVGs; no personal contact details.")


if __name__ == "__main__":
    main()
