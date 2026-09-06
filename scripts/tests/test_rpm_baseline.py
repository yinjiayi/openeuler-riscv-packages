# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import hashlib
import importlib.util
import inspect
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock


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


def network_document(
    network_id: str,
    name: str,
    session: str,
    *,
    internal: bool,
    containers: set[str],
) -> dict[str, object]:
    return {
        "Id": network_id,
        "Name": name,
        "Driver": "bridge",
        "Scope": "local",
        "Internal": internal,
        "Attachable": False,
        "Ingress": False,
        "Labels": {
            MODULE.RUNNER_MANAGED_NETWORK_LABEL: MODULE.RUNNER_MANAGED_VALUE,
            MODULE.RUNNER_SESSION_LABEL: session,
        },
        "Containers": {container: {} for container in containers},
    }


def container_document(
    container_id: str,
    name: str,
    session: str,
    networks: dict[str, str],
) -> dict[str, object]:
    return {
        "Id": container_id,
        "Name": f"/{name}",
        "Config": {
            "Image": "image@sha256:" + "f" * 64,
            "Labels": {
                MODULE.RUNNER_MANAGED_LABEL: MODULE.RUNNER_MANAGED_VALUE,
                MODULE.RUNNER_SESSION_LABEL: session,
            }
        },
        "HostConfig": {"NetworkMode": next(iter(networks.values()), "none")},
        "State": {"Running": False},
        "NetworkSettings": {
            "Networks": {
                network_name: {"NetworkID": network_id}
                for network_name, network_id in networks.items()
            }
        },
    }


class RpmBaselineEvidenceTests(unittest.TestCase):
    def test_image_baseline_probe_is_networkless_read_only_and_never_pulls(self) -> None:
        with mock.patch.object(
            MODULE,
            "run",
            return_value="rpm\t0:4.18-1\triscv64\nbash\t0:5.2-1\triscv64\n",
        ) as mocked:
            manifest = MODULE.rpm_manifest_from_image("image@sha256:" + "a" * 64)
        self.assertEqual(manifest[0].split("\t", 1)[0], "bash")
        argv = mocked.call_args.args[0]
        self.assertIn("--pull", argv)
        self.assertEqual(argv[argv.index("--pull") + 1], "never")
        self.assertEqual(argv[argv.index("--network") + 1], "none")
        self.assertIn("--read-only", argv)
        self.assertTrue(mocked.call_args.kwargs["capture"])

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
        self.assertEqual(
            evidence["network_phase"], "network-absent-before-install"
        )
        self.assertFalse(evidence["network_install_completed"])

    def test_missing_anchor_and_malformed_entry_fail_closed(self) -> None:
        manifest = [entry(name) for name in sorted(MODULE.BASELINE_ANCHORS - {"rpm-build"})]
        manifest.append("not-a-three-field-rpm-record")
        evidence = MODULE.rpm_baseline_evidence("demo", "image@sha256:" + "a" * 64, manifest)
        self.assertEqual(evidence["status"], "failed")
        self.assertEqual(evidence["missing_anchors"], ["rpm-build"])
        self.assertEqual(evidence["malformed_entry_count"], 1)

    def test_egress_container_is_created_only_after_networkless_baseline(self) -> None:
        source = PREPARE.read_text(encoding="utf-8")
        probe = source.index("before = rpm_manifest_from_image")
        baseline = source.index("baseline = rpm_baseline_evidence", probe)
        rejection = source.index('if baseline["status"] != "passed"', baseline)
        egress_create = source.index('egress_network_id = run([', rejection)
        create = source.index('"docker", "create"', egress_create)
        connected = source.index('baseline["network_install_started"] = True', create)
        persisted = source.index("write_json_atomic(baseline_path, baseline)", connected)
        install = source.index("run(root_exec(", persisted)
        verified = source.index('transaction_record.get("status") != "passed"', install)
        disconnect = source.index(
            '["docker", "network", "disconnect", egress_network_id, container_id]',
            verified,
        )
        self.assertIn(
            '"--platform", "linux/riscv64", "--network", "none", "--read-only"',
            inspect.getsource(MODULE.rpm_manifest_from_image),
        )
        self.assertNotIn('"docker", "network", "connect"', source)
        self.assertLess(probe, baseline)
        self.assertLess(baseline, rejection)
        self.assertLess(rejection, egress_create)
        self.assertLess(egress_create, create)
        self.assertLess(create, connected)
        self.assertLess(connected, persisted)
        self.assertLess(persisted, install)
        self.assertLess(install, verified)
        self.assertLess(verified, disconnect)

    def test_connected_state_is_atomically_persisted_before_install(self) -> None:
        manifest = [entry(name) for name in sorted(MODULE.BASELINE_ANCHORS)]
        evidence = MODULE.rpm_baseline_evidence("demo", "image@sha256:" + "a" * 64, manifest)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "rpm-baseline.json"
            MODULE.write_json_atomic(path, evidence)
            initial = json.loads(path.read_text(encoding="utf-8"))
            self.assertFalse(initial["network_install_started"])
            self.assertEqual(
                initial["network_phase"], "network-absent-before-install"
            )

            evidence["network_install_started"] = True
            evidence["network_phase"] = "exclusive-egress-verified-before-install"
            MODULE.write_json_atomic(path, evidence)
            connected = json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(connected["network_install_started"])
            self.assertEqual(
                connected["network_phase"], "exclusive-egress-verified-before-install"
            )
            self.assertEqual(list(path.parent.glob(f".{path.name}.*.tmp")), [])

    def test_egress_creation_failure_cannot_claim_network_started(self) -> None:
        source = PREPARE.read_text(encoding="utf-8")
        create = source.index("egress_network_id = run([")
        connected = source.index('baseline["network_install_started"] = True', create)
        persisted = source.index("write_json_atomic(baseline_path, baseline)", connected)
        self.assertLess(create, connected)
        self.assertLess(connected, persisted)
        self.assertIn("check=True", inspect.getsource(MODULE.run))

    def test_managed_network_requires_exact_internal_identity_and_exclusivity(self) -> None:
        network_id = "a" * 64
        container_id = "b" * 64
        session = "c" * 32
        document = network_document(
            network_id,
            "isolated",
            session,
            internal=True,
            containers={container_id},
        )
        evidence = MODULE.validate_managed_network(
            document,
            expected_id=network_id,
            expected_name="isolated",
            expected_internal=True,
            expected_session=session,
            expected_containers={container_id},
        )
        self.assertTrue(evidence["internal"])
        self.assertEqual(evidence["exclusive_container_count"], 1)

        for key, value in (("Internal", False), ("Driver", "host"), ("Scope", "swarm")):
            invalid = dict(document)
            invalid[key] = value
            with self.subTest(key=key), self.assertRaises(SystemExit):
                MODULE.validate_managed_network(
                    invalid,
                    expected_id=network_id,
                    expected_name="isolated",
                    expected_internal=True,
                    expected_session=session,
                    expected_containers={container_id},
                )

    def test_container_networks_must_match_both_names_and_full_ids(self) -> None:
        container_id = "a" * 64
        isolated_id = "b" * 64
        egress_id = "c" * 64
        session = "d" * 32
        document = container_document(
            container_id,
            "builddeps",
            session,
            {"isolated": isolated_id, "egress": egress_id},
        )
        self.assertEqual(
            MODULE.validate_container_networks(
                document,
                expected_id=container_id,
                expected_name="builddeps",
                expected_session=session,
                expected_networks={"isolated": isolated_id, "egress": egress_id},
            ),
            container_id,
        )
        with self.assertRaisesRegex(SystemExit, "unexpected network endpoints"):
            MODULE.validate_container_networks(
                document,
                expected_id=container_id,
                expected_name="builddeps",
                expected_session=session,
                expected_networks={"egress": egress_id},
            )

    def test_empty_dependency_container_requires_none_network_mode(self) -> None:
        container_id = "a" * 64
        session = "b" * 32
        document = container_document(container_id, "builddeps", session, {})
        self.assertEqual(
            MODULE.validate_container_networks(
                document,
                expected_id=container_id,
                expected_name="builddeps",
                expected_session=session,
                expected_networks=None,
            ),
            container_id,
        )
        document["HostConfig"]["NetworkMode"] = "bridge"
        with self.assertRaisesRegex(SystemExit, "external endpoint"):
            MODULE.validate_container_networks(
                document,
                expected_id=container_id,
                expected_name="builddeps",
                expected_session=session,
                expected_networks=None,
            )

    def test_cleanup_attempts_exact_resources_and_reports_failures(self) -> None:
        first = "a" * 64
        second = "b" * 64
        outcomes = [0, 0, 1, 0]
        with mock.patch.object(
            MODULE.subprocess,
            "run",
            side_effect=[SimpleNamespace(returncode=code) for code in outcomes],
        ) as mocked:
            failures = MODULE.cleanup_docker_resources(
                "c" * 64,
                container_created=True,
                started=True,
                network_ids=[first, second],
            )
        self.assertEqual(failures, [f"network-remove:{first}"])
        commands = [call.args[0] for call in mocked.call_args_list]
        self.assertEqual(commands[0][:3], ["docker", "stop", "--time"])
        self.assertEqual(commands[0][-1], "c" * 64)
        self.assertEqual(commands[1], ["docker", "rm", "--force", "c" * 64])
        self.assertEqual(commands[2], ["docker", "network", "rm", first])
        self.assertEqual(commands[3], ["docker", "network", "rm", second])

    def test_malformed_create_output_recovers_exact_labelled_object_ids(self) -> None:
        network_id = "a" * 64
        container_id = "b" * 64
        session = "c" * 32
        network = network_document(
            network_id,
            "egress",
            session,
            internal=False,
            containers=set(),
        )
        container = container_document(
            container_id,
            "builddeps",
            session,
            {"egress": network_id},
        )
        with mock.patch.object(MODULE, "inspect_network", return_value=network):
            self.assertEqual(
                MODULE.recover_created_network_id(
                    "warning mixed into stdout",
                    expected_name="egress",
                    expected_internal=False,
                    expected_session=session,
                ),
                network_id,
            )
        with mock.patch.object(MODULE, "inspect_container", return_value=container):
            self.assertEqual(
                MODULE.recover_created_container_id(
                    "truncated",
                    expected_name="builddeps",
                    expected_image="image@sha256:" + "f" * 64,
                    expected_network_mode=network_id,
                    expected_network_name="egress",
                    expected_session=session,
                ),
                container_id,
            )

    def test_create_recovery_refuses_identity_mismatch(self) -> None:
        network_id = "a" * 64
        session = "b" * 32
        network = network_document(
            network_id,
            "egress",
            "wrong-session",
            internal=False,
            containers=set(),
        )
        with mock.patch.object(MODULE, "inspect_network", return_value=network):
            with self.assertRaisesRegex(SystemExit, "identity or isolation"):
                MODULE.recover_created_network_id(
                    "malformed",
                    expected_name="egress",
                    expected_internal=False,
                    expected_session=session,
                )

    def test_cleanup_continues_after_command_exception(self) -> None:
        network_id = "a" * 64
        with mock.patch.object(
            MODULE.subprocess,
            "run",
            side_effect=[OSError("docker unavailable"), SimpleNamespace(returncode=0)],
        ) as mocked:
            failures = MODULE.cleanup_docker_resources(
                "b" * 64,
                container_created=False,
                started=True,
                network_ids=[network_id],
            )
        self.assertEqual(failures, ["container-stop"])
        self.assertEqual(len(mocked.call_args_list), 2)


class RpmBaselineImageContractTests(unittest.TestCase):
    def test_bootstrap_and_target_share_one_query_format_helper(self) -> None:
        helper = MANIFEST_HELPER.read_text(encoding="utf-8")
        self.assertIn("%{SHA1HEADER}", helper)
        self.assertIn("%{SHA256HEADER}", helper)
        self.assertIn("NF != 5", helper)
        self.assertIn("length($4) != 40", helper)
        self.assertIn("length($5) != 64", helper)
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
        self.assertIn("%{SHA256HEADER}", MANIFEST_HELPER.read_text(encoding="utf-8"))

    def test_large_authenticated_bootstrap_downloads_resume_before_checksum_use(self) -> None:
        bootstrap = BOOTSTRAP.read_text(encoding="utf-8")
        helper = bootstrap.index("download_verified_resumable()")
        resume = bootstrap.index("--continue-at -", helper)
        bounded_attempts = bootstrap.index("for attempt in 1 2 3 4 5", helper)
        checksum = bootstrap.index("sha256sum --check --strict", helper)
        publish = bootstrap.index('mv -f -- "$partial" "$output"', checksum)
        self.assertLess(helper, resume)
        self.assertLess(resume, checksum)
        self.assertLess(bounded_attempts, checksum)
        self.assertLess(checksum, publish)
        self.assertIn(
            '"${repo_url}${primary_href}" "$primary_checksum" /evidence/primary.sqlite.bz2',
            bootstrap,
        )
        self.assertIn(
            '"${repo_url}${key_href}" "$key_checksum" /evidence/openEuler-gpg-keys.rpm',
            bootstrap,
        )
        self.assertIn('rm -f -- "$output" "$partial"', bootstrap)
        self.assertNotIn('--retry 4 --retry-delay 2 --connect-timeout 20 --max-time 300', bootstrap)

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
