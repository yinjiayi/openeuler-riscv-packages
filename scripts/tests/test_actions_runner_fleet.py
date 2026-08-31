# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import stat
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
OPS = ROOT / "ops" / "actions-runner-fleet"


def parse_assignment_file(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        key, value = line.split("=", 1)
        result[key] = value
    return result


class RunnerFleetStaticTests(unittest.TestCase):
    def test_fleet_is_one_runner_per_host_with_reviewed_stages(self) -> None:
        fleet = json.loads((OPS / "fleet.json").read_text(encoding="utf-8"))
        self.assertEqual(fleet["host_last_octet"], {"first": 201, "last": 250})
        self.assertEqual(fleet["runners_per_host"], 1)
        self.assertEqual(fleet["rollout"]["canary_last_octets"], [201, 202, 203, 204, 205])
        self.assertEqual(fleet["rollout"]["conditional_last_octets"], [211, 220, 224, 231])
        self.assertEqual(fleet["rollout"]["clean_host_count_including_canary"], 46)

    def test_runner_release_is_exactly_locked(self) -> None:
        lock = parse_assignment_file(OPS / "runner-release.lock")
        self.assertEqual(lock["RUNNER_VERSION"], "2.336.0")
        self.assertEqual(lock["RUNNER_SIZE"], "226035903")
        self.assertEqual(
            lock["RUNNER_SHA256"],
            "04cf0be1aff4c3ec3554466c39124ca250e3effd8873bb7e8d68535aa9505d5d",
        )
        self.assertEqual(
            lock["RUNNER_URL"],
            "https://github.com/actions/runner/releases/download/v2.336.0/"
            "actions-runner-linux-x64-2.336.0.tar.gz",
        )

    def test_cleanup_image_matches_repository_digest_lock(self) -> None:
        cleanup = parse_assignment_file(OPS / "cleanup-image.lock")["CLEANUP_IMAGE_REF"]
        image_lock = (ROOT / "ci" / "image.lock").read_text(encoding="utf-8")
        image = re.search(r"^image:\s*([^\s]+)$", image_lock, re.MULTILINE)
        digest = re.search(r'^digest:\s*"(sha256:[0-9a-f]{64})"$', image_lock, re.MULTILINE)
        self.assertIsNotNone(image)
        self.assertIsNotNone(digest)
        self.assertEqual(cleanup, f"{image.group(1)}@{digest.group(1)}")
        cleanup_script = (OPS / "cleanup.sh").read_text(encoding="utf-8")
        self.assertIn("--pull never", cleanup_script)
        self.assertIn("--network none", cleanup_script)
        self.assertIn('--managed-image-ref "$CLEANUP_IMAGE_REF"', cleanup_script)
        self.assertLess(
            cleanup_script.index("oe_load_cleanup_image_lock"),
            cleanup_script.index("docker-cleanup.py"),
        )
        self.assertNotIn("src=$runner_dir", cleanup_script)

    def test_dependency_containers_have_the_recovery_identity_label(self) -> None:
        prepare = (ROOT / "ci" / "prepare-build-deps.py").read_text(encoding="utf-8")
        cleanup = (OPS / "docker-cleanup.py").read_text(encoding="utf-8")
        marker = "io.openeuler.actions-runner.managed-builddeps"
        self.assertIn(marker, prepare)
        self.assertIn(marker, cleanup)
        self.assertIn('"--label", f"{RUNNER_MANAGED_LABEL}={RUNNER_MANAGED_VALUE}"', prepare)

    def test_systemctl_global_options_precede_the_verb(self) -> None:
        for filename in ("activate.sh", "audit.sh", "register.sh"):
            script = (OPS / filename).read_text(encoding="utf-8")
            self.assertNotRegex(script, r"oe_systemctl is-(?:active|enabled) --quiet")
        audit = (OPS / "audit.sh").read_text(encoding="utf-8")
        self.assertIn('oe_systemctl --quiet is-active "$service"', audit)
        self.assertIn('oe_systemctl --quiet is-enabled "$service"', audit)

    def test_systemctl_package_integrity_precedes_every_lifecycle_call(self) -> None:
        library = (OPS / "_lib.sh").read_text(encoding="utf-8")
        installer = (OPS / "install.sh").read_text(encoding="utf-8")
        preflight = (OPS / "preflight.sh").read_text(encoding="utf-8")
        audit = (OPS / "audit.sh").read_text(encoding="utf-8")

        integrity = library.split("oe_assert_systemctl_integrity() {", 1)[1].split(
            "\n}", 1
        )[0]
        self.assertIn("[[ -f $oe_systemctl_path && ! -L $oe_systemctl_path", integrity)
        self.assertIn("root:root:755", integrity)
        self.assertIn('systemd: /usr/bin/systemctl', integrity)
        self.assertIn("${binary:Package}\\t${Status}\\t${Version}", integrity)
        self.assertIn("dpkg-query --verify systemd", integrity)
        self.assertIn("[[ -z $verification ]]", integrity)
        self.assertNotIn("mctes", library)

        platform = library.split("oe_assert_platform() {", 1)[1].split("\n}", 1)[0]
        self.assertLess(
            platform.index("oe_assert_systemctl_integrity"),
            platform.index("oe_systemctl is-system-running"),
        )
        wrapper = library.split("oe_systemctl() {", 1)[1].split("\n}", 1)[0]
        self.assertLess(
            wrapper.index("oe_assert_systemctl_integrity"),
            wrapper.index('oe_run "$oe_systemctl_path"'),
        )
        package_install = installer.index("apt-get install -y --no-install-recommends")
        post_apt_integrity = installer.index("oe_assert_systemctl_integrity", package_install)
        self.assertLess(package_install, post_apt_integrity)
        self.assertLess(post_apt_integrity, installer.index("oe_systemctl daemon-reload"))
        self.assertIn('oe_assert_platform "$OE_IDENTITY_ALLOW_DEGRADED"', preflight)
        self.assertIn('oe_assert_platform "$OE_ARG_ALLOW_DEGRADED"', audit)

        for path in sorted(OPS.glob("*.sh")):
            if path.name == "_lib.sh":
                continue
            self.assertNotRegex(
                path.read_text(encoding="utf-8"),
                r"(?m)^\s*systemctl(?:\s|$)",
                path.name,
            )

    def test_policy_has_only_two_main_workflows_and_two_events(self) -> None:
        policy = parse_assignment_file(OPS / "policy.conf")
        slug = "yinjiayi/openeuler-riscv-packages"
        self.assertEqual(policy["OE_RUNNER_ENROLLMENT_ENABLED"], "false")
        self.assertEqual(policy["OE_RUNNER_ALLOWED_REF"], "refs/heads/main")
        self.assertEqual(policy["OE_RUNNER_ALLOWED_EVENTS"], "push,workflow_dispatch")
        self.assertEqual(
            policy["OE_RUNNER_ALLOWED_WORKFLOW_REFS"].split(","),
            [
                f"{slug}/.github/workflows/package-ci.yml@refs/heads/main",
                f"{slug}/.github/workflows/rpm-repo-backfill.yml@refs/heads/main",
            ],
        )
        guard = (OPS / "job-guard.sh").read_text(encoding="utf-8")
        for rejected in ("pull_request", "pull_request_target", "merge_group", "workflow_run"):
            self.assertIn(rejected, guard)

    def test_registration_retains_default_labels_and_has_no_token_argv(self) -> None:
        helper = (OPS / "credential_exec.py").read_text(encoding="utf-8")
        self.assertNotIn("--no-default-labels", helper)
        self.assertIn('"--labels",', helper)
        self.assertIn('"ACTIONS_RUNNER_INPUT_TOKEN": token', helper)
        self.assertNotRegex(helper, r"child_argv[\s\S]{0,2500}[\"']--token[\"']")
        self.assertNotIn("native-riscv", helper)
        workflow = (ROOT / ".github" / "workflows" / "package-ci.yml").read_text(
            encoding="utf-8"
        )
        for label in ("self-hosted", "linux", "x64", "oe-rva23-qemu"):
            self.assertIn(label, workflow)

    def test_installer_uses_ubuntu_runuser_group_initialization(self) -> None:
        installer = (OPS / "install.sh").read_text(encoding="utf-8")
        self.assertIn(
            'runuser --user "$oe_runner_user" -- docker info',
            installer,
        )
        self.assertNotIn("runuser --user \"$oe_runner_user\" --groups", installer)
        self.assertIn('usermod --append --groups docker "$oe_runner_user"', installer)

    def test_installer_provisions_the_docker_iptables_frontend(self) -> None:
        installer = (OPS / "install.sh").read_text(encoding="utf-8")
        preflight = (OPS / "preflight.sh").read_text(encoding="utf-8")
        package_block = installer.split(
            "apt-get install -y --no-install-recommends", 1
        )[1].split("\n\n", 1)[0]

        self.assertRegex(package_block, r"(?:^|\s)iptables(?:\s|$)")
        self.assertNotRegex(package_block, r"(?:^|\s)nftables(?:\s|$)")
        iptables_probe = "[[ -x /usr/sbin/iptables ]]"
        alternatives_repair = "update-alternatives --auto iptables"
        self.assertIn(alternatives_repair, package_block)
        self.assertIn("readlink -- /usr/sbin/iptables", package_block)
        self.assertIn("/etc/alternatives/iptables", package_block)
        self.assertIn(iptables_probe, preflight)
        self.assertLess(
            installer.index("apt-get install -y --no-install-recommends"),
            installer.index(alternatives_repair),
        )
        self.assertLess(
            installer.index(alternatives_repair),
            installer.index("readlink -- /usr/sbin/iptables"),
        )

    def test_fleet_audit_is_installed_with_machine_only_stdout(self) -> None:
        installer = (OPS / "install.sh").read_text(encoding="utf-8")
        audit = (OPS / "audit.sh").read_text(encoding="utf-8")
        fleet_audit = (OPS / "fleet-audit.py").read_text(encoding="utf-8")

        self.assertIn('"$source_dir/audit.sh"', installer)
        self.assertIn(
            '"$oe_runner_libexec/preflight.sh" --name "$OE_ARG_NAME" >&2',
            audit,
        )
        self.assertIn(
            '"/usr/local/libexec/openeuler-actions-runner/audit.sh"',
            fleet_audit,
        )

    def test_cleanup_lock_survives_root_activation_then_runner_hooks(self) -> None:
        library = (OPS / "_lib.sh").read_text(encoding="utf-8")
        installer = (OPS / "install.sh").read_text(encoding="utf-8")
        cleanup = (OPS / "cleanup.sh").read_text(encoding="utf-8")
        audit = (OPS / "audit.sh").read_text(encoding="utf-8")
        unit = (OPS / "openeuler-actions-runner@.service").read_text(encoding="utf-8")

        self.assertIn("oe_runner_lock_dir=$oe_runner_base/.locks", library)
        self.assertIn('"$oe_runner_base" "$oe_runner_lock_dir"', installer)
        self.assertIn(
            'install -o root -g "$oe_runner_group" -m 0660 /dev/null "$cleanup_lock"',
            installer,
        )
        self.assertIn('cleanup_lock=$oe_runner_lock_dir/$name.lock', cleanup)
        self.assertIn('root:"$oe_runner_group":660', cleanup)
        self.assertIn('exec 9<>"$cleanup_lock"', cleanup)
        self.assertNotIn('cleanup_lock=$state_dir/cleanup.lock', cleanup)
        self.assertIn('cleanup_lock=$oe_runner_lock_dir/$OE_ARG_NAME.lock', audit)
        self.assertIn(
            "ReadWritePaths=/opt/openeuler-actions-runner/.locks", unit
        )

    def test_job_start_cleanup_preserves_runner_managed_action_state(self) -> None:
        library = (OPS / "_lib.sh").read_text(encoding="utf-8")
        cleanup = (OPS / "cleanup.sh").read_text(encoding="utf-8")
        started = (OPS / "job-started.sh").read_text(encoding="utf-8")
        completed = (OPS / "job-completed.sh").read_text(encoding="utf-8")
        activate = (OPS / "activate.sh").read_text(encoding="utf-8")

        self.assertIn("oe_job_workspace()", library)
        self.assertIn('workspace=$(oe_job_workspace "$runner_dir/_work" "$PWD")', started)
        self.assertIn('--phase job-start --workspace "$workspace"', started)
        self.assertIn('cleanup_work=$workspace', cleanup)
        self.assertIn('src=$cleanup_work,dst=/cleanup/work', cleanup)
        self.assertNotIn('src=$work_dir,dst=/cleanup/work', cleanup)
        self.assertIn('cd -- "$runner_dir"', completed)
        self.assertLess(completed.index('cd -- "$runner_dir"'), completed.index("cleanup.sh"))
        self.assertIn('--phase before', activate)

    def test_runner_uniqueness_allows_only_the_managed_lock_directory(self) -> None:
        library = (OPS / "_lib.sh").read_text(encoding="utf-8")

        self.assertIn('"$runner_dir"|"$oe_runner_lock_dir") ;;', library)
        self.assertIn(
            '*) oe_die "another runner directory exists: $directory" ;;',
            library,
        )

    def test_service_sandbox_permits_only_required_network_families(self) -> None:
        unit = (OPS / "openeuler-actions-runner@.service").read_text(encoding="utf-8")
        self.assertIn(
            "RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6 AF_NETLINK",
            unit,
        )
        self.assertNotIn("AF_PACKET", unit)
        self.assertNotIn("AF_RAW", unit)
        preflight = (OPS / "preflight.sh").read_text(encoding="utf-8")
        library = (OPS / "_lib.sh").read_text(encoding="utf-8")
        self.assertIn("oe_assert_local_host", preflight)
        self.assertIn("ip -o -4 address show scope global", library)

    def test_service_sandbox_preserves_runner_action_tar_extraction(self) -> None:
        unit = (OPS / "openeuler-actions-runner@.service").read_text(encoding="utf-8")
        self.assertIn("NoNewPrivileges=true", unit)
        self.assertIn("CapabilityBoundingSet=", unit)
        self.assertIn("AmbientCapabilities=", unit)
        self.assertIn("RestrictSUIDSGID=false", unit)
        self.assertNotIn("RestrictSUIDSGID=true", unit)

        preflight = (OPS / "preflight.sh").read_text(encoding="utf-8")
        self.assertIn(".tar-extract-preflight.", preflight)
        self.assertIn('mkdir "$tar_probe_dir/source"', preflight)
        self.assertIn(
            'tar -czf "$tar_probe_dir/preflight.tar.gz" -C "$tar_probe_dir" source',
            preflight,
        )
        self.assertIn('tar -xzf "$tar_probe_dir/preflight.tar.gz"', preflight)
        self.assertIn('cmp -s "$oe_runner_libexec/preflight.sh"', preflight)
        self.assertIn(
            '[[ -x $tar_probe_dir/extracted/source/preflight.sh ]]', preflight
        )
        self.assertIn("trap cleanup_tar_probe EXIT", preflight)

    def test_installed_runner_version_probes_use_the_service_identity(self) -> None:
        library = (OPS / "_lib.sh").read_text(encoding="utf-8")
        self.assertIn("oe_runner_version()", library)
        self.assertIn('runuser --user "$oe_runner_user"', library)
        self.assertIn("exec \"${2:?}\" --version", library)
        for filename in ("install.sh", "register.sh", "preflight.sh", "audit.sh"):
            source = (OPS / filename).read_text(encoding="utf-8")
            self.assertIn("oe_runner_version", source, filename)
            self.assertNotRegex(
                source,
                r'runner_dir/bin/Runner\.Listener["}]?"? --version',
                filename,
            )

    def test_shell_and_python_sources_parse_and_are_executable(self) -> None:
        for path in sorted(OPS.glob("*.sh")):
            completed = subprocess.run(
                ["bash", "-n", str(path)], capture_output=True, text=True, check=False
            )
            self.assertEqual(completed.returncode, 0, f"{path}: {completed.stderr}")
            self.assertTrue(path.stat().st_mode & stat.S_IXUSR, f"not executable: {path}")
        for path in sorted(OPS.glob("*.py")):
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
            self.assertTrue(path.stat().st_mode & stat.S_IXUSR, f"not executable: {path}")

    def test_shell_guard_regressions(self) -> None:
        completed = subprocess.run(
            ["bash", str(OPS / "tests" / "test-lib.sh")],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("shell guards passed", completed.stdout)

    def test_activate_has_explicit_enable_and_failure_rollback(self) -> None:
        script = (OPS / "activate.sh").read_text(encoding="utf-8")
        self.assertIn("--enable-reviewed-policy", script)
        self.assertIn("rollback_activation", script)
        self.assertIn("oe_systemctl disable --now", script)
        self.assertIn('OE_RUNNER_ENROLLMENT_ENABLED=false', script)
        self.assertLess(script.index("cleanup.sh"), script.index("policy_changed=false"))

    def test_conditional_permission_is_persisted_and_used_by_preflight(self) -> None:
        library = (OPS / "_lib.sh").read_text(encoding="utf-8")
        preflight = (OPS / "preflight.sh").read_text(encoding="utf-8")
        activate = (OPS / "activate.sh").read_text(encoding="utf-8")
        self.assertIn("ALLOW_DEGRADED=%s", library)
        self.assertIn("OE_IDENTITY_ALLOW_DEGRADED", library)
        self.assertIn('oe_assert_platform "$OE_IDENTITY_ALLOW_DEGRADED"', preflight)
        self.assertIn(
            '[[ $OE_IDENTITY_ALLOW_DEGRADED == "$OE_ARG_ALLOW_DEGRADED" ]]', activate
        )
        self.assertNotIn("oe_assert_platform false", preflight)

    def test_no_literal_github_credential_or_test_command_override(self) -> None:
        token = re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})")
        for path in OPS.rglob("*"):
            if path.is_file():
                value = path.read_text(encoding="utf-8")
                self.assertIsNone(token.search(value), f"credential-shaped literal in {path}")
                self.assertNotIn("OE_RUNNER_COMMAND_PREFIX", value)


class DockerCleanupTests(unittest.TestCase):
    image = (
        "ghcr.io/yinjiayi/openeuler-riscv64-rpmbuild@sha256:"
        + "c9d8e675e04cd0ef61c5b2e77d530652db79de51431dc047277cdbd1f63b32b3"
    )

    def make_fake_docker(self, directory: Path) -> tuple[Path, Path]:
        executable = directory / "docker"
        log = directory / "docker.log"
        executable.write_text(
            """#!/bin/sh
set -eu
printf '%s\\n' "$*" >>"$FAKE_DOCKER_LOG"
case "$*" in
  "ps --no-trunc --quiet")
    if [ "${FAKE_RUNNING:-0}" != 0 ] && ! grep -q '^rm --force --volumes -- aaaaaaaaaaaa$' "$FAKE_DOCKER_LOG"; then
      printf '%s\\n' aaaaaaaaaaaa
      if [ "${FAKE_CHANGED:-0}" = 1 ] && [ "$(grep -c '^ps --no-trunc --quiet$' "$FAKE_DOCKER_LOG")" -gt 1 ]; then
        printf '%s\\n' dddddddddddd
      fi
    fi
    ;;
  "inspect --format {{json .}} aaaaaaaaaaaa")
    if [ "${FAKE_MANAGED:-0}" = 1 ]; then
      printf '%s\\n' "$FAKE_MANAGED_INSPECT"
    else
      printf '%s\\n' '{"Id":"aaaaaaaaaaaa","Name":"/unrelated","Config":{},"HostConfig":{"AutoRemove":false},"State":{"Running":true}}'
    fi
    ;;
  "ps --all --quiet") printf '%s\\n' bbbbbbbbbbbb ;;
  "image ls --all --format {{.Repository}}:{{.Tag}} --filter reference=openeuler-builddeps:*")
    printf '%s\\n' openeuler-builddeps:12345-1
    ;;
  "volume ls --quiet --filter dangling=true") printf '%s\\n' runner-volume ;;
  "network ls --quiet --filter type=custom") printf '%s\\n' cccccccccccc ;;
  "network inspect --format {{len .Containers}} cccccccccccc") printf '0\\n' ;;
  "rm --force --volumes -- aaaaaaaaaaaa"|\
  "rm --force --volumes -- bbbbbbbbbbbb"|\
  "volume rm --force -- runner-volume"|\
  "network rm -- cccccccccccc"|\
  "image rm --force -- openeuler-builddeps:12345-1") : ;;
  *) printf 'unexpected fake Docker command: %s\\n' "$*" >&2; exit 2 ;;
esac
""",
            encoding="utf-8",
        )
        executable.chmod(0o755)
        return executable, log

    def run_helper(
        self, running: bool, managed: bool = False, changed: bool = False
    ) -> tuple[subprocess.CompletedProcess[str], list[str]]:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            docker, log = self.make_fake_docker(directory)
            environment = dict(os.environ)
            environment["FAKE_DOCKER_LOG"] = str(log)
            environment["FAKE_RUNNING"] = "1" if running else "0"
            environment["FAKE_MANAGED"] = "1" if managed else "0"
            environment["FAKE_CHANGED"] = "1" if changed else "0"
            environment["FAKE_MANAGED_INSPECT"] = json.dumps(
                {
                    "Id": "aaaaaaaaaaaa",
                    "Name": "/openeuler-builddeps-12345-1a2b3c4d",
                    "Config": {
                        "Image": self.image,
                        "Cmd": ["/bin/bash", "-c", "while :; do sleep 3600; done"],
                        "Labels": {
                            "io.openeuler.actions-runner.managed-builddeps": "v1"
                        },
                    },
                    "HostConfig": {"AutoRemove": False},
                    "State": {"Running": True},
                },
                separators=(",", ":"),
            )
            completed = subprocess.run(
                [
                    str(OPS / "docker-cleanup.py"),
                    "--docker",
                    str(docker),
                    "--max-objects",
                    "8",
                    "--managed-image-ref",
                    self.image,
                ],
                capture_output=True,
                text=True,
                env=environment,
                check=False,
            )
            commands = log.read_text(encoding="utf-8").splitlines()
            return completed, commands

    def test_idle_dedicated_host_cleanup_is_bounded_and_specific(self) -> None:
        completed, commands = self.run_helper(running=False)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["removed_managed_running_containers"], 0)
        self.assertEqual(result["removed_containers"], 1)
        self.assertEqual(result["removed_dangling_volumes"], 1)
        self.assertEqual(result["removed_unused_networks"], 1)
        self.assertEqual(result["removed_derived_images"], 1)
        self.assertIn("rm --force --volumes -- bbbbbbbbbbbb", commands)
        self.assertIn("volume rm --force -- runner-volume", commands)
        self.assertIn("network rm -- cccccccccccc", commands)
        self.assertIn("image rm --force -- openeuler-builddeps:12345-1", commands)
        joined = "\n".join(commands)
        self.assertNotIn("image prune", joined)
        self.assertNotIn("builder prune", joined)
        self.assertNotIn("ghcr.io/", joined)

    def test_running_container_fails_before_every_mutation(self) -> None:
        completed, commands = self.run_helper(running=True)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("unrecognized running container", completed.stderr)
        self.assertEqual(
            commands,
            ["ps --no-trunc --quiet", "inspect --format {{json .}} aaaaaaaaaaaa"],
        )

    def test_labeled_managed_running_container_is_recovered(self) -> None:
        completed, commands = self.run_helper(running=True, managed=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["removed_managed_running_containers"], 1)
        self.assertIn("rm --force --volumes -- aaaaaaaaaaaa", commands)

    def test_changed_running_inventory_fails_before_mutation(self) -> None:
        completed, commands = self.run_helper(running=True, managed=True, changed=True)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("inventory changed during inspection", completed.stderr)
        self.assertNotIn("rm --force --volumes -- aaaaaaaaaaaa", commands)


if __name__ == "__main__":
    unittest.main()
