# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import hashlib
import importlib.util
import inspect
import json
from pathlib import Path
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[2]
PREPARE = REPO / "ci" / "prepare-build-deps.py"
MANIFEST_HELPER = REPO / "ci" / "rpm-manifest.sh"
FINALIZER = REPO / "ci" / "finalize-target-rpmdb.sh"
VERIFY = REPO / "ci" / "verify-target.sh"
BOOTSTRAP = REPO / "ci" / "bootstrap-rootfs.sh"
CONTAINERFILE = REPO / "ci" / "Containerfile.riscv64"
IMAGE_WORKFLOW = REPO / ".github" / "workflows" / "build-ci-image.yml"
BOOTSTRAP_REPOSITORY = REPO / "ci" / "openeuler-rva23.repo"

SPEC = importlib.util.spec_from_file_location("prepare_build_deps_baseline", PREPARE)
if SPEC is None or SPEC.loader is None:
    raise AssertionError(f"cannot load {PREPARE}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def entry(name: str) -> str:
    return f"{name}\t0:1.0-1\triscv64"


class RpmBaselineEvidenceTests(unittest.TestCase):
    def test_complete_live_baseline_is_checksum_bound(self) -> None:
        manifest = [entry(name) for name in sorted(MODULE.BASELINE_ANCHORS)]
        evidence = MODULE.rpm_baseline_evidence("demo", "image@sha256:" + "a" * 64, manifest)
        self.assertEqual(evidence["status"], "passed")
        self.assertEqual(evidence["classification"], "none")
        self.assertEqual(evidence["missing_anchors"], [])
        self.assertFalse(evidence["network_install_started"])
        expected = hashlib.sha256(("\n".join(manifest) + "\n").encode()).hexdigest()
        self.assertEqual(evidence["rpm_manifest_before_sha256"], expected)

    def test_empty_baseline_fails_closed_before_networking(self) -> None:
        evidence = MODULE.rpm_baseline_evidence("demo", "image@sha256:" + "a" * 64, [])
        self.assertEqual(evidence["status"], "failed")
        self.assertEqual(evidence["classification"], "failure:infrastructure")
        self.assertEqual(evidence["reason"], "base-image-rpm-baseline-invalid")
        self.assertEqual(evidence["missing_anchors"], sorted(MODULE.BASELINE_ANCHORS))
        self.assertFalse(evidence["network_install_started"])
        self.assertEqual(evidence["network_phase"], "disconnected-before-install")

    def test_missing_anchor_and_malformed_entry_fail_closed(self) -> None:
        manifest = [entry(name) for name in sorted(MODULE.BASELINE_ANCHORS - {"rpm-build"})]
        manifest.append("not-a-three-field-rpm-record")
        evidence = MODULE.rpm_baseline_evidence("demo", "image@sha256:" + "a" * 64, manifest)
        self.assertEqual(evidence["status"], "failed")
        self.assertEqual(evidence["missing_anchors"], ["rpm-build"])
        self.assertEqual(evidence["malformed_entry_count"], 1)

    def test_network_is_absent_until_after_baseline_validation(self) -> None:
        source = PREPARE.read_text(encoding="utf-8")
        create = source.index('"docker", "create"')
        network_none = source.index('"--network", "none"', create)
        baseline = source.index("baseline = rpm_baseline_evidence", network_none)
        rejection = source.index('if baseline["status"] != "passed"', baseline)
        connect = source.index('["docker", "network", "connect", "bridge", container]', rejection)
        connected = source.index('baseline["network_install_started"] = True', connect)
        persisted = source.index("write_json_atomic(baseline_path, baseline)", connected)
        install = source.index("install_attempts = run_with_retries", persisted)
        self.assertLess(create, network_none)
        self.assertLess(network_none, baseline)
        self.assertLess(baseline, rejection)
        self.assertLess(rejection, connect)
        self.assertLess(connect, connected)
        self.assertLess(connected, persisted)
        self.assertLess(persisted, install)

    def test_connected_state_is_atomically_persisted_before_install(self) -> None:
        manifest = [entry(name) for name in sorted(MODULE.BASELINE_ANCHORS)]
        evidence = MODULE.rpm_baseline_evidence("demo", "image@sha256:" + "a" * 64, manifest)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "rpm-baseline.json"
            MODULE.write_json_atomic(path, evidence)
            initial = json.loads(path.read_text(encoding="utf-8"))
            self.assertFalse(initial["network_install_started"])
            self.assertEqual(initial["network_phase"], "disconnected-before-install")

            evidence["network_install_started"] = True
            evidence["network_phase"] = "connected-before-install"
            MODULE.write_json_atomic(path, evidence)
            connected = json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(connected["network_install_started"])
            self.assertEqual(connected["network_phase"], "connected-before-install")
            self.assertEqual(list(path.parent.glob(f".{path.name}.*.tmp")), [])

    def test_connect_failure_cannot_claim_network_started(self) -> None:
        source = PREPARE.read_text(encoding="utf-8")
        connect = source.index('["docker", "network", "connect", "bridge", container]')
        connected = source.index('baseline["network_install_started"] = True', connect)
        persisted = source.index("write_json_atomic(baseline_path, baseline)", connected)
        self.assertLess(connect, connected)
        self.assertLess(connected, persisted)
        self.assertIn("check=True", inspect.getsource(MODULE.run))


class RpmBaselineImageContractTests(unittest.TestCase):
    def test_bootstrap_and_target_share_one_query_format_helper(self) -> None:
        helper = MANIFEST_HELPER.read_text(encoding="utf-8")
        self.assertIn("%{SIGPGP:pgpsig}", helper)
        self.assertIn("%{SHA1HEADER}", helper)
        self.assertIn("%{SHA256HEADER}", helper)
        self.assertIn("--dbpath", helper)
        self.assertIn("dbpath_components", helper)
        self.assertIn('/bootstrap/rpm-manifest.sh "$rootfs"', BOOTSTRAP.read_text(encoding="utf-8"))
        self.assertIn('"$manifest_helper" >"$live_manifest"', VERIFY.read_text(encoding="utf-8"))

    def test_target_verification_requires_nonempty_exact_anchored_manifest(self) -> None:
        verify = VERIFY.read_text(encoding="utf-8")
        self.assertIn('[[ -s $live_manifest ]]', verify)
        self.assertIn("bash rpm rpm-build gcc gcc-c++ make python3", verify)
        self.assertIn('cmp -s -- "$manifest" "$live_manifest"', verify)

    def test_finalizer_uses_evaluated_paths_and_never_guesses_a_symlink(self) -> None:
        finalizer = FINALIZER.read_text(encoding="utf-8")
        bootstrap = BOOTSTRAP.read_text(encoding="utf-8")
        self.assertIn("rpm --root \"$rootfs\" --eval '%{_dbpath}'", bootstrap)
        self.assertIn("rpm --eval '%{_dbpath}'", finalizer)
        self.assertIn("rpmdb paths overlap", finalizer)
        self.assertIn("the target runtime rpmdb path is unexpectedly nonempty", finalizer)
        self.assertIn('rmdir "$runtime_db"', finalizer)
        self.assertIn('mv -- "$staging_db" "$runtime_db"', finalizer)
        self.assertNotIn('find "$runtime_db" -mindepth 1 -delete', finalizer)
        self.assertNotIn('cp -a -- "$staging_db/." "$runtime_db/"', finalizer)
        self.assertNotIn("ln -s", finalizer)
        self.assertNotIn("/var/lib/rpm", finalizer)
        self.assertNotIn("/usr/lib/sysimage/rpm", finalizer)

    def test_target_rpm_imports_the_verified_portable_header_stream(self) -> None:
        finalizer = FINALIZER.read_text(encoding="utf-8")
        bootstrap = BOOTSTRAP.read_text(encoding="utf-8")
        for marker in (
            'rpmdb --root "$rootfs" --verifydb',
            'rpmdb --root "$rootfs" --exportdb',
            'rpmdb --dbpath "$roundtrip_db" --importdb',
            'rpmdb --dbpath "$roundtrip_db" --exportdb',
            'cmp -s /evidence/rpmdb-header-list.bin /evidence/rpmdb-header-list-roundtrip.bin',
        ):
            self.assertIn(marker, bootstrap)
        for marker in (
            'rpmdb --dbpath "$staging_db" --importdb',
            'rpmdb --dbpath "$staging_db" --verifydb',
            '"$manifest_helper" --dbpath "$staging_db"',
            'cmp -s -- "$baseline_root/rpm-manifest.tsv" "$staging_manifest"',
            'cmp -s -- "$baseline_root/rpm-manifest.tsv" "$runtime_manifest"',
            "rpmdb --verifydb",
        ):
            self.assertIn(marker, finalizer)
        self.assertNotIn('cmp -s -- "$transport" "$target_export"', finalizer)
        for forbidden in ("--initdb", "--justdb", "--nodeps", "--nosignature", "dnf "):
            self.assertNotIn(forbidden, finalizer)

    def test_transport_originates_after_the_signed_dependency_transaction(self) -> None:
        bootstrap = BOOTSTRAP.read_text(encoding="utf-8")
        repository = BOOTSTRAP_REPOSITORY.read_text(encoding="utf-8")
        transaction = bootstrap.index("dnf -y")
        export = bootstrap.index('rpmdb --root "$rootfs" --exportdb')
        self.assertLess(transaction, export)
        self.assertIn("gpgcheck=1", repository)
        self.assertIn("gpgkey=file://", repository)
        self.assertIn("%{SIGPGP:pgpsig}", MANIFEST_HELPER.read_text(encoding="utf-8"))

    def test_target_finalization_runs_before_exact_target_verification(self) -> None:
        containerfile = CONTAINERFILE.read_text(encoding="utf-8")
        finalizer = containerfile.index("finalize-target-rpmdb.sh")
        execution = containerfile.index("&& /usr/local/libexec/openeuler-riscv-ci/finalize-target-rpmdb.sh")
        verification = containerfile.index("&& /usr/local/bin/verify-target", execution)
        self.assertLess(finalizer, execution)
        self.assertLess(execution, verification)

    def test_image_workflow_tracks_and_hashes_both_baseline_helpers(self) -> None:
        workflow = IMAGE_WORKFLOW.read_text(encoding="utf-8")
        for name in ("ci/finalize-target-rpmdb.sh", "ci/rpm-manifest.sh"):
            self.assertGreaterEqual(workflow.count(f"- {name}"), 2)
            self.assertIn(f"sha256sum {name}", workflow)
        self.assertIn("artifacts/image/rpm-manifest-live.tsv", workflow)
        self.assertIn(
            "cmp -s artifacts/image/rpm-manifest.tsv artifacts/image/rpm-manifest-live.tsv",
            workflow,
        )


if __name__ == "__main__":
    unittest.main()
