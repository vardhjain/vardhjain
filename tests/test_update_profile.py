import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import update_profile as profile


def repo(name, **overrides):
    return {"name": name, "owner": {"login": "vardhjain"}, "private": False,
            "visibility": "public", "fork": False, "archived": False,
            "pushed_at": "2026-10-30T12:30:00Z", **overrides}


def metrics():
    return {"commit": "a" * 40, "generated_at": "2026-10-30T04:00:00+00:00",
            "exposure": {"tools_total": 29},
            "tests": {"passed": 281, "failed": 0, "coverage_pct": 94.92}}


class SnapshotTests(unittest.TestCase):
    def collect(self, repos=None):
        with patch.object(profile, "get_json", side_effect=[repos or [repo(n) for n in profile.FEATURED], metrics()]):
            return profile.collect()

    def test_public_only_and_original_projects(self):
        repos = [repo(n) for n in profile.FEATURED] + [
            repo("secret", private=True), repo("fork", fork=True),
            repo("archive", archived=True), repo("vardhjain"),
            repo("someone-elses", owner={"login": "someone"})]
        self.assertEqual(self.collect(repos)["public_projects"], 4)

    def test_pagination_is_complete(self):
        first = [repo(n) for n in profile.FEATURED] + [repo(f"project-{i}") for i in range(96)]
        with patch.object(profile, "get_json", side_effect=[first, [repo("page-two")], metrics()]) as get:
            snapshot = profile.collect()
        self.assertEqual(snapshot["public_projects"], 101)
        self.assertIn("page=2", get.call_args_list[1].args[0])

    def test_duplicate_pagination_fails_instead_of_overcounting(self):
        first = [repo(n) for n in profile.FEATURED] + [repo(f"project-{i}") for i in range(96)]
        with patch.object(profile, "get_json", side_effect=[first, [first[0]]]):
            with self.assertRaisesRegex(ValueError, "Duplicate"):
                profile.collect()

    def test_recent_activity_is_curated_and_sorted(self):
        repos = [repo(n) for n in profile.FEATURED]
        repos[0]["pushed_at"] = "2026-10-31T12:30:00Z"
        snapshot = self.collect(repos + [repo("unfeatured", pushed_at="2026-11-01T00:00:00Z")])
        self.assertEqual(snapshot["recent"][0]["name"], repos[0]["name"])
        self.assertEqual(len(snapshot["recent"]), 3)
        self.assertNotIn("unfeatured", [r["name"] for r in snapshot["recent"]])

    def test_invalid_metrics_and_timestamps_are_rejected(self):
        data = self.collect()
        for field, value in [("coverage_pct", 101), ("coverage_pct", float("nan")),
                             ("tests_passed", -1), ("tests_passed", True),
                             ("tools", 1.5), ("commit", "not-a-sha"),
                             ("measured_at", "2026-10-30T04:00:00")]:
            invalid = copy.deepcopy(data)
            invalid["mcp"][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                profile.validate(invalid)

    def test_source_failure_never_writes_files(self):
        with patch.object(profile, "get_json", side_effect=OSError("API unavailable")), \
                patch.object(profile.os, "replace") as replace, \
                patch.object(sys, "argv", ["update_profile.py"]):
            with self.assertRaises(OSError):
                profile.main()
            replace.assert_not_called()

    def test_markers_preserve_handwritten_profile(self):
        original = f"Intro\n{profile.START}\nOld\n{profile.END}\nProjects"
        updated = profile.replace_section(original, profile.render_section(self.collect()))
        self.assertTrue(updated.startswith("Intro\n"))
        self.assertTrue(updated.endswith("\nProjects"))
        for bad in ["no markers", original + profile.START, profile.END + profile.START]:
            with self.assertRaises(ValueError):
                profile.replace_section(bad, "replacement")

    def test_cards_are_accessible_xml_and_text_is_escaped(self):
        for mobile in [False, True]:
            svg = ET.fromstring(profile.render_card(self.collect(), mobile))
            self.assertEqual(svg.attrib["role"], "img")
            self.assertIn("281", "".join(svg.itertext()))
        self.assertIn("&lt;script&gt;", profile.text(0, 0, "<script>"))

    def test_snapshot_rebuild_is_deterministic(self):
        data = self.collect()
        readme = f"{profile.START}\nOld\n{profile.END}"
        first = profile.outputs(data, readme)
        second = profile.outputs(data, first["README.md"])
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
