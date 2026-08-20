# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import importlib.machinery
import importlib.util
import pathlib
import unittest


REPO = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "dispatch-trusted-package-ci"
AUTHORIZER = REPO / "ci" / "authorize-trusted-package-dispatch.py"
LOADER = importlib.machinery.SourceFileLoader("trusted_package_dispatch", str(SCRIPT))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
assert SPEC is not None
MODULE = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(MODULE)
AUTHORIZER_LOADER = importlib.machinery.SourceFileLoader("trusted_package_dispatch_authorizer", str(AUTHORIZER))
AUTHORIZER_SPEC = importlib.util.spec_from_loader(AUTHORIZER_LOADER.name, AUTHORIZER_LOADER)
assert AUTHORIZER_SPEC is not None
AUTHORIZER_MODULE = importlib.util.module_from_spec(AUTHORIZER_SPEC)
AUTHORIZER_LOADER.exec_module(AUTHORIZER_MODULE)


class TrustedPackageDispatchTests(unittest.TestCase):
    def pr(self, **overrides):
        document = {
            "state": "open",
            "head": {
                "repo": {"full_name": "yinjiayi/openeuler-riscv-packages"},
                "ref": "onboard/demo-1.0",
                "sha": "a" * 40,
            },
            "base": {"ref": "main", "sha": "b" * 40},
            "user": {"login": "yinjiayi"},
            "author_association": "OWNER",
            "changed_files": 2,
            "html_url": "https://example.invalid/pr/1",
        }
        document.update(overrides)
        return document

    def files(self):
        return [
            {"filename": "packages/demo/package.yaml"},
            {"filename": "packages/demo/demo.spec"},
        ]

    def test_accepts_exact_same_repository_package_pr(self):
        result = MODULE.trusted_pr(self.pr(), self.files(), "demo", "yinjiayi/openeuler-riscv-packages")
        self.assertEqual(result["head_sha"], "a" * 40)
        self.assertEqual(MODULE.run_name(123, "a" * 40), "Package CI PR 123 " + "a" * 40)

    def test_rejects_fork_untrusted_author_and_non_package_scope(self):
        fork = self.pr()
        fork["head"] = dict(fork["head"])
        fork["head"]["repo"] = {"full_name": "attacker/openeuler-riscv-packages"}
        with self.assertRaisesRegex(MODULE.ToolError, "trusted repository"):
            MODULE.trusted_pr(fork, self.files(), "demo", "yinjiayi/openeuler-riscv-packages")

        author = self.pr(author_association="CONTRIBUTOR", user={"login": "attacker"})
        with self.assertRaisesRegex(MODULE.ToolError, "author is not trusted"):
            MODULE.trusted_pr(author, self.files(), "demo", "yinjiayi/openeuler-riscv-packages")

        files = self.files() + [{"filename": ".github/workflows/package-ci.yml"}]
        scope = self.pr(changed_files=3)
        with self.assertRaisesRegex(MODULE.ToolError, "confined"):
            MODULE.trusted_pr(scope, files, "demo", "yinjiayi/openeuler-riscv-packages")

    def test_final_result_must_bind_the_requested_head_and_package(self):
        document = {"package_id": "demo", "commit_sha": "a" * 40, "status": "passed", "classification": "none"}
        MODULE.verify_build_result(document, "demo", "a" * 40)
        document["commit_sha"] = "b" * 40
        with self.assertRaisesRegex(MODULE.ToolError, "does not bind"):
            MODULE.verify_build_result(document, "demo", "a" * 40)


class TrustedPackageDispatchAuthorizerTests(unittest.TestCase):
    def pr(self, **overrides):
        document = {
            "state": "open",
            "head": {
                "repo": {"full_name": "yinjiayi/openeuler-riscv-packages"},
                "ref": "repair/demo-1.0",
                "sha": "a" * 40,
            },
            "base": {"ref": "main", "sha": "b" * 40},
            "user": {"login": "yinjiayi"},
            "author_association": "OWNER",
            "changed_files": 2,
        }
        document.update(overrides)
        return document

    def files(self):
        return [
            {"filename": "packages/demo/package.yaml"},
            {"filename": "packages/demo/demo.spec"},
        ]

    def authorize(self, **overrides):
        values = {
            "repo": "yinjiayi/openeuler-riscv-packages",
            "package_id": "demo",
            "base_sha": "b" * 40,
            "head_sha": "a" * 40,
            "publish_to_repo": "false",
            "event_ref": "refs/heads/main",
        }
        values.update(overrides)
        AUTHORIZER_MODULE.authorize(self.pr(), self.files(), **values)

    def test_accepts_exact_open_trusted_package_pr(self):
        self.authorize()

    def test_rejects_unbound_head_publication_and_scope(self):
        with self.assertRaisesRegex(AUTHORIZER_MODULE.AuthorizationError, "does not match"):
            self.authorize(head_sha="c" * 40)
        with self.assertRaisesRegex(AUTHORIZER_MODULE.AuthorizationError, "disable repository publication"):
            self.authorize(publish_to_repo="true")
        with self.assertRaisesRegex(AUTHORIZER_MODULE.AuthorizationError, "protected main"):
            self.authorize(event_ref="refs/heads/repair/demo")

        files = self.files() + [{"filename": "ci/compose-build-result.py"}]
        with self.assertRaisesRegex(AUTHORIZER_MODULE.AuthorizationError, "confined"):
            AUTHORIZER_MODULE.authorize(
                self.pr(changed_files=3),
                files,
                repo="yinjiayi/openeuler-riscv-packages",
                package_id="demo",
                base_sha="b" * 40,
                head_sha="a" * 40,
                publish_to_repo="false",
                event_ref="refs/heads/main",
            )


if __name__ == "__main__":
    unittest.main()
