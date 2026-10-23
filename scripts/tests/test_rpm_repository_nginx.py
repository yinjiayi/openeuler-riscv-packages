# SPDX-License-Identifier: Apache-2.0
"""Static deployment-config contracts; these are not real HTTP/Nginx tests."""
from pathlib import Path
import re
import shlex
import unittest


REPO = Path(__file__).resolve().parents[2]
CONFIG = REPO / "ops/rpm-repo-server/nginx.conf"
INSTALLER = REPO / "ops/rpm-repo-server/install.sh"
VARIABLE = "$openeuler_rpmrepo_generation_cache_control"
IMMUTABLE = "public, max-age=31536000, immutable"


class GenerationCachePolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        # Ignore comments, including the documentation's http{} spelling.
        self.config = "\n".join(
            line for line in CONFIG.read_text(encoding="utf-8").splitlines()
            if not line.lstrip().startswith("#")
        )

    def block(self, directive: str) -> str:
        matches = list(re.finditer(re.escape(directive) + r"\s*\{", self.config))
        self.assertEqual(len(matches), 1, directive)
        start = matches[0].end()
        end = self.config.find("}", start)
        self.assertNotEqual(end, -1)
        body = self.config[start:end]
        self.assertNotIn("{", body)
        return body

    def test_only_content_statuses_are_immutable(self) -> None:
        directive = f"map $status {VARIABLE}"
        body = self.block(directive)
        prefix = self.config[:self.config.index(directive)]
        self.assertEqual(prefix.count("{"), prefix.count("}"), "map must be at HTTP level")
        self.assertLess(self.config.index(directive), self.config.index("server {"))
        rows = [shlex.split(row) for row in body.split(";") if row.strip()]
        self.assertEqual(rows.count(["volatile"]), 1)
        rows = [row for row in rows if row != ["volatile"]]
        self.assertTrue(all(len(row) == 2 for row in rows))
        policy = dict(rows)
        self.assertEqual(len(rows), len(policy), "duplicate map entries")
        self.assertEqual(policy, {"default": "no-store", "200": IMMUTABLE,
                                  "206": IMMUTABLE, "304": IMMUTABLE})
        # Include redirects, denied/missing paths, method/range errors and 5xx.
        for status in range(100, 600):
            with self.subTest(status=status):
                expected = IMMUTABLE if status in (200, 206, 304) else "no-store"
                self.assertEqual(policy.get(str(status), policy["default"]), expected)

    def test_generation_header_uses_status_map_even_for_errors(self) -> None:
        body = self.block("location /generations/")
        self.assertIn("try_files $uri $uri/ =404;", body)
        headers = re.findall(r"add_header\s+Cache-Control\s+([^;]+);", body)
        self.assertEqual(headers, [f"{VARIABLE} always"])
        self.assertIn("add_header X-Content-Type-Options nosniff always;", body)

    def test_late_range_errors_re_evaluate_status_map(self) -> None:
        # A cached initial 200 must not be reused when the filter sees 416.
        # This static guard does not prove native header-filter ordering or
        # eliminate a header already appended before the range was rejected.
        body = self.block(f"map $status {VARIABLE}")
        self.assertRegex(body, r"(?m)^\s*volatile\s*;")

    def test_hidden_denials_keep_no_store_and_nosniff_fallback(self) -> None:
        server_headers = self.config.split("server {", 1)[1].split("location", 1)[0]
        self.assertIn('add_header Cache-Control "no-store" always;', server_headers)
        self.assertIn("add_header X-Content-Type-Options nosniff always;", server_headers)
        deny = self.block(r"location ~ /\.")
        self.assertIn("deny all;", deny)
        self.assertNotIn("add_header", deny, "denial must inherit both safe server headers")
        self.assertNotIn("location ^~ /generations/", self.config)

    def test_mutable_and_ordinary_paths_keep_their_existing_policy(self) -> None:
        self.assertIn('add_header Cache-Control "no-store" always;',
                      self.block("location = /state.json"))
        self.assertIn('add_header Cache-Control "no-cache" always;',
                      self.block("location /"))

    def test_installer_keeps_http_include_and_checks_before_restart(self) -> None:
        installer = INSTALLER.read_text(encoding="utf-8")
        self.assertIn('"$source_dir/nginx.conf" /etc/nginx/sites-available/openeuler-rpmrepo',
                      installer)
        self.assertIn("/etc/nginx/sites-enabled/openeuler-rpmrepo", installer)
        self.assertLess(installer.index("nginx -t"), installer.index("systemctl restart nginx"))


if __name__ == "__main__":
    unittest.main()
