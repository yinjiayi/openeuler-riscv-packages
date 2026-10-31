# SPDX-License-Identifier: Apache-2.0
import copy
import json
import pathlib
import runpy
import shutil
import tempfile
import unittest
from unittest.mock import patch

from helpers import SCRIPTS, run_tool, write_json
from test_dashboard_history_generator import GEN, history, published_fixture

GATE = runpy.run_path(str(SCRIPTS.parent / "ci/validate-dashboard-output.py"))


class DashboardOutputGateTests(unittest.TestCase):
    def test_iri_display_links_are_encoded_without_reinterpreting_templates(self):
        link = GEN["http_link"]
        self.assertEqual(link("https://tklab.eu1.netbird.services/file/My stuff"),
                         "https://tklab.eu1.netbird.services/file/My%20stuff")
        self.assertEqual(link("https://appli.réseau-constellation.ca"),
                         "https://appli.xn--rseau-constellation-bzb.ca")
        self.assertEqual(link("https://example.org/日本語?q=été#資料"),
                         "https://example.org/%E6%97%A5%E6%9C%AC%E8%AA%9E?q=%C3%A9t%C3%A9#%E8%B3%87%E6%96%99")
        self.assertEqual(link("https://example.org/a%20b?x=1&y=2"), "https://example.org/a%20b?x=1&y=2")
        self.assertEqual(link("http://[::1]:8080/a"), "http://[::1]:8080/a")
        for unsafe in ("https://example.org/${pkgname}", "https://example.org/end}",
                       "https://example.org/%{provider_prefix}", "https://user:secret@example.org",
                       "https://example.org/\npath", "https://exa mple.org/path", "https://example.org:99999",
                       "https://example.org/%ZZ", "javascript:alert(1)", "https://example.org\\path", "https://[v1.fe]/a"):
            with self.subTest(unsafe=unsafe):
                self.assertIsNone(link(unsafe))
        raw = {"discovery_key": "demo", "names": ["demo"], "upstream_urls": ["https://example.org/${pkgname}"]}
        original = copy.deepcopy(raw)
        row = GEN["inventory_row"](raw, None, None, None)
        self.assertEqual(raw, original)
        self.assertEqual(row["name"], "demo")
        self.assertIn("invalid-upstream-link", row["decisions"])
        self.assertNotIn("upstream", row.get("links", {}))

    def fixture(self, root):
        write_json(root / "packages/demo/package.yaml", {"package_id": "demo", "rpm": {"name": "demo"}, "version": {"current": "1.0"}})
        (root / "dashboard").mkdir()
        for name in ("index.html", "app.js", "styles.css"):
            shutil.copyfile(SCRIPTS.parent / "dashboard" / name, root / "dashboard" / name)
        hist = root / "history.json"
        write_json(hist, history([]))
        pub = root / "published-state.json"
        write_json(pub, published_fixture())
        output = root / "public"
        run_tool("generate-dashboard", ["--repo-root", str(root), "--build-history", str(hist),
                 "--output-dir", str(output), "--now", "2026-10-09T00:01:00Z"], root)
        return output, pub

    def test_all_json_gate_positive_invalid_uri_timestamp_and_browser_mismatch(self):
        import jsonschema
        with tempfile.TemporaryDirectory() as directory:
            output, pub = self.fixture(pathlib.Path(directory))
            accepted = GATE["validate"](output, pub)
            self.assertEqual(accepted["status"], "passed")
            self.assertEqual(len(accepted["files"]), 5)
            extra = output / "extra.json"
            extra.write_text("malformed JSON")
            with self.assertRaisesRegex(ValueError, "unexpected or missing generated JSON"):
                GATE["validate"](output, pub)
            extra.unlink()
            inventory = json.loads((output / "inventory.json").read_text())
            inventory["entries"].append({"inventory_id": "demo", "name": "demo", "version": "1", "status": "discovered", "links": {"upstream": "https://example.org/a b"}})
            write_json(output / "inventory.json", inventory)
            with self.assertRaises(jsonschema.ValidationError):
                GATE["validate"](output, pub)
            inventory["entries"] = []
            inventory["generated_at"] = "not a timestamp"
            write_json(output / "inventory.json", inventory)
            with self.assertRaises(jsonschema.ValidationError):
                GATE["validate"](output, pub)
            inventory["generated_at"] = "2026-10-09T00:01:00Z"
            write_json(output / "inventory.json", inventory)
            write_json(output / "build-history.json", {})
            with self.assertRaisesRegex(ValueError, "browser history differs"):
                GATE["validate"](output, pub)

    def test_missing_uri_handler_never_silently_passes(self):
        import jsonschema
        checker = jsonschema.FormatChecker()
        checker.checkers.pop("uri", None)
        with tempfile.TemporaryDirectory() as directory:
            output, pub = self.fixture(pathlib.Path(directory))
            with patch.object(jsonschema, "FormatChecker", return_value=checker):
                with self.assertRaisesRegex(ValueError, "format handlers unavailable: uri"):
                    GATE["validate"](output, pub)

    def test_noop_uri_handler_fails_negative_control(self):
        import jsonschema
        checker = jsonschema.FormatChecker()
        checker.checkers["uri"] = (lambda value: True, ())
        with patch.object(jsonschema, "FormatChecker", return_value=checker):
            with self.assertRaisesRegex(ValueError, "format control failed: uri"):
                GATE["format_checker"]({"type": "string", "format": "uri"})


if __name__ == "__main__":
    unittest.main()
