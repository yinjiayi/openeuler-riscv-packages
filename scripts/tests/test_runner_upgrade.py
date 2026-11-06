# SPDX-License-Identifier: Apache-2.0
"""Offline upgrade safety fixtures; never invoke host lifecycle operations."""
import datetime
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import tarfile
import tempfile
import sys
import types
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "ops/actions-runner-fleet/upgrade.sh"
SOURCE = SCRIPT.read_text()
EMBEDDED = SOURCE.split("<<'PY_UPGRADE'\n", 1)[1].split("\nPY_UPGRADE", 1)[0]
MODULE = types.ModuleType("upgrade_fixture")
exec(compile(EMBEDDED, str(SCRIPT), "exec"), MODULE.__dict__)


class UpgradePayloadTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        original = MODULE.verify_payload
        self.verify = lambda directory, records: original(directory, records, os.getuid(), os.getgid())
        patch = mock.patch.object(MODULE, "verify_payload", self.verify)
        patch.start()
        self.addCleanup(patch.stop)

    def archive(self, version="old", extra=None, reverse=False):
        path = self.root / (version + ".tar.gz")
        entries = []
        for name in sorted(MODULE.TOPS):
            entries.append((name, "dir" if name in {"bin", "externals"} else "file", version.encode()))
        entries += [("bin/Runner.Listener", "file", version.encode()),
                    ("externals/node", "dir", b""),
                    ("externals/lib", "dir", b""),
                    ("externals/lib/tool.js", "file", version.encode()),
                    ("externals/node/tool", "link", "../lib/tool.js")]
        entries += extra or []
        if reverse:
            entries.reverse()
        with tarfile.open(path, "w:gz") as stream:
            for name, kind, value in entries:
                item = tarfile.TarInfo(name)
                item.mode = 0o755 if kind in {"file", "dir"} else 0o777
                if kind == "dir":
                    item.type = tarfile.DIRTYPE
                elif kind in {"link", "hardlink"}:
                    item.type = tarfile.SYMTYPE if kind == "link" else tarfile.LNKTYPE
                    item.linkname = value
                else:
                    item.size = len(value)
                stream.addfile(item, io.BytesIO(value) if kind == "file" else None)
        return path, hashlib.sha256(path.read_bytes()).hexdigest(), path.stat().st_size

    def extract(self, version, destination):
        args = self.archive(version)
        records = MODULE.archive_records(*args)
        MODULE.extract_payload(args[0], destination, records)
        return records

    def test_safe_relative_symlink_and_private_umask_extract(self):
        args = self.archive()
        records = MODULE.archive_records(*args)
        previous = os.umask(0o077)
        try:
            MODULE.extract_payload(args[0], self.root / "payload", records)
        finally:
            os.umask(previous)
        self.verify(self.root / "payload", records)
        self.assertEqual((self.root / "payload/externals/node/tool").read_bytes(), b"old")
        self.assertEqual(stat.S_IMODE((self.root / "payload/bin").stat().st_mode), 0o755)

    def test_reversed_physical_order_streams_once_without_backward_seek(self):
        args = self.archive("reverse", reverse=True)
        records = MODULE.archive_records(*args)
        with tarfile.open(args[0], "r:gz") as stream:
            physical_order = [member.name for member in stream]
        self.assertNotEqual(physical_order, sorted(records, key=lambda name: (name.count("/"), name)))
        self.assertLess(physical_order.index("externals/lib/tool.js"), physical_order.index("externals"))
        real_open = tarfile.open
        modes, offsets = [], []

        def forward_only_open(path, mode):
            modes.append(mode)
            self.assertEqual(mode, "r|gz")
            stream = real_open(path, mode)
            real_seek = stream.fileobj.seek

            def forward_only_seek(offset):
                self.assertGreaterEqual(offset, stream.fileobj.pos, "gzip extraction sought backwards")
                offsets.append(offset)
                return real_seek(offset)

            stream.fileobj.seek = forward_only_seek
            return stream

        with mock.patch.object(MODULE.tarfile, "open", side_effect=forward_only_open), \
             mock.patch.object(tarfile.TarFile, "getmembers", side_effect=AssertionError("random-access member index forbidden")):
            MODULE.extract_payload(args[0], self.root / "streamed", records)
        self.assertEqual(modes, ["r|gz"])
        self.assertTrue(offsets, "the stream's forward-only seek guard was not exercised")
        self.verify(self.root / "streamed", records)

    def test_streaming_extraction_rejects_archive_drift_after_audit(self):
        original, sha, size = self.archive()
        records = MODULE.archive_records(original, sha, size)
        for change in ("extra", "missing", "duplicate", "unsafe", "type", "mode", "size", "link", "bytes"):
            with self.subTest(change=change):
                changed = self.root / (change + ".tar.gz")
                with tarfile.open(original, "r:gz") as source, tarfile.open(changed, "w:gz") as output:
                    for member in source:
                        data = source.extractfile(member).read() if member.isfile() else None
                        if member.name == "bin/Runner.Listener":
                            if change == "missing":
                                continue
                            if change == "type":
                                member.type, member.size, data = tarfile.DIRTYPE, 0, None
                            elif change == "unsafe":
                                member.name = "../escape"
                            elif change == "mode":
                                member.mode ^= 0o020
                            elif change == "size":
                                member.size += 1
                                data += b"!"
                            elif change == "bytes":
                                data = b"bad"
                        if change == "link" and member.issym():
                            member.linkname = "../lib/unreviewed.js"
                        output.addfile(member, io.BytesIO(data) if data is not None else None)
                        if change == "duplicate" and member.name == "bin/Runner.Listener":
                            output.addfile(member, io.BytesIO(data))
                    if change == "extra":
                        member = tarfile.TarInfo("bin/unreviewed")
                        member.mode, member.size = 0o755, 1
                        output.addfile(member, io.BytesIO(b"x"))
                with self.assertRaises(ValueError):
                    MODULE.extract_payload(changed, self.root / change, records)

    def test_bad_hash_and_size_fail_before_extract(self):
        path, sha, size = self.archive()
        for bad_sha, bad_size in [("0" * 64, size), (sha, size + 1)]:
            with self.subTest(sha=bad_sha, size=bad_size), self.assertRaisesRegex(ValueError, "mismatch"):
                MODULE.archive_records(path, bad_sha, bad_size)

    def test_archive_rejects_traversal_special_duplicate_and_escaping_links(self):
        invalid = [("../escape", "file", b"x"), ("/absolute", "file", b"x"),
                   ("bin/../escape", "file", b"x"), ("config.sh", "file", b"again"),
                   ("bin/link", "hardlink", "config.sh"),
                   ("bin/link", "link", "/etc/passwd"),
                   ("bin/link", "link", "../../etc/passwd"),
                   ("bin/link", "link", "../config.sh"),
                   ("externals/link", "link", "missing")]
        for index, entry in enumerate(invalid):
            with self.subTest(entry=entry), self.assertRaises(ValueError):
                MODULE.archive_records(*self.archive(str(index), [entry]))

    def test_complete_old_payload_detects_modified_extra_and_wrong_type(self):
        for mode in ("bytes", "extra", "link"):
            with self.subTest(mode=mode):
                destination = self.root / mode
                records = self.extract(mode, destination)
                listener = destination / "bin/Runner.Listener"
                if mode == "bytes":
                    listener.write_bytes(b"changed")
                elif mode == "extra":
                    (destination / "bin/old-leftover").write_bytes(b"stale")
                else:
                    listener.unlink()
                    listener.symlink_to("../config.sh")
                with self.assertRaises(ValueError):
                    self.verify(destination, records)

    def preserved(self, runner):
        for name in MODULE.RUNTIME:
            (runner / name).mkdir(mode=0o700)
            (runner / name / "user-data").write_bytes(b"not official payload")
        for name in MODULE.CONFIGURATION:
            (runner / name).write_bytes(b"fixture secret; never open in production")
            (runner / name).chmod(0o640)
        return {str(p.relative_to(runner)): (p.lstat().st_ino, p.lstat().st_mode, p.read_bytes() if p.is_file() else None)
                for top in MODULE.RUNTIME | MODULE.CONFIGURATION
                for p in [runner / top, *((runner / top).rglob("*") if (runner / top).is_dir() else [])]}

    def test_payload_only_upgrade_keeps_registration_runtime_and_old_backup(self):
        runner, staged, backup = self.root / "runner", self.root / "stage", self.root / "backup"
        old_records = self.extract("old", runner)
        new_records = self.extract("new", staged)
        retained = self.preserved(runner)
        (runner / ".release").write_text("old release")
        backup.mkdir(mode=0o700)
        MODULE.replace_payload(runner, staged, backup, new_records)
        self.verify(runner, new_records)
        self.verify(backup / "payload", old_records)
        for name, expected in retained.items():
            p = runner / name
            self.assertEqual((p.lstat().st_ino, p.lstat().st_mode, p.read_bytes() if p.is_file() else None), expected)
        self.assertIn("version=2.338.2", (runner / ".release").read_text())

    def test_partial_replacement_can_restore_all_old_roots_without_restart(self):
        runner, staged, backup = self.root / "runner", self.root / "stage", self.root / "backup"
        old_records = self.extract("old", runner)
        new_records = self.extract("new", staged)
        retained = self.preserved(runner)
        (runner / ".release").write_text("old release")
        backup.mkdir(mode=0o700)
        real_replace = os.replace
        installed = 0

        def interrupted(source, destination):
            nonlocal installed
            if Path(source).parent == staged:
                installed += 1
                if installed == 2:
                    raise OSError("simulated interrupted payload transaction")
            return real_replace(source, destination)

        with mock.patch.object(MODULE.os, "replace", interrupted), self.assertRaises(OSError):
            MODULE.replace_payload(runner, staged, backup, new_records)
        MODULE.restore_payload(runner, backup)
        self.verify(runner, old_records)
        self.assertEqual((runner / ".release").read_text(), "old release")
        for name, expected in retained.items():
            p = runner / name
            self.assertEqual((p.lstat().st_ino, p.lstat().st_mode, p.read_bytes() if p.is_file() else None), expected)
        self.assertTrue(list(backup.glob("failed-payload-*")))

    def proof(self):
        prepared = {"host": "10.230.50.201", "name": "oe-rva23-qemu-201", "runner_id": 24,
                    "nonce": "n" * 64, "source_commit": "a" * 40, "prepared_at": 1000}
        proof = {"schema_version": 1, "kind": "runner-upgrade-offline-observation", "repository": MODULE.REPO,
                 "host": prepared["host"], "name": prepared["name"], "runner_id": 24,
                 "prepared_nonce": prepared["nonce"], "source_commit": prepared["source_commit"],
                 "old_version": MODULE.OLD_VERSION, "new_version": MODULE.NEW_VERSION, "new_sha256": MODULE.NEW_SHA,
                 "status": "offline", "busy": False,
                 "observed_at": datetime.datetime.fromtimestamp(1100, datetime.timezone.utc).isoformat()}
        return prepared, proof

    def test_fresh_exact_identity_offline_observation(self):
        prepared, proof = self.proof()
        MODULE.verify_observation(proof, prepared, 1200)

    def test_receipt_rejects_wrong_identity_scope_version_busy_stale_and_future(self):
        prepared, good = self.proof()
        changes = {"host": "10.230.50.202", "runner_id": 25, "name": "different", "repository": "other/repo",
                   "source_commit": "b" * 40, "prepared_nonce": "old-nonce", "status": "online", "busy": True,
                   "old_version": "2.335.0", "new_version": "latest", "new_sha256": "0" * 64}
        for key, value in changes.items():
            with self.subTest(field=key), self.assertRaises(ValueError):
                MODULE.verify_observation({**good, key: value}, prepared, 1200)
        for timestamp in (999, 1201, 899):
            with self.subTest(timestamp=timestamp), self.assertRaises(ValueError):
                MODULE.verify_observation({**good, "observed_at": datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).isoformat()}, prepared, 1200)
        with self.assertRaises(ValueError):
            MODULE.verify_observation(good, prepared, 1401)
        with self.assertRaises(ValueError):
            MODULE.verify_observation({**good, "busy": 0}, prepared, 1200)

    def test_root_private_receipt_and_state_required(self):
        path = self.root / "receipt.json"
        path.write_text("{}")
        path.chmod(0o644)
        with self.assertRaises(ValueError):
            MODULE.trusted_path(path, private=True)

    def test_dotnet_public_identity_accepts_bom_and_binds_name_id(self):
        path = self.root / ".runner"
        document = {"agentId": 24, "agentName": "oe-rva23-qemu-201", "disableUpdate": True,
                    "gitHubUrl": "https://github.com/" + MODULE.REPO, "workFolder": "_work"}
        path.write_text(json.dumps(document), encoding="utf-8-sig")
        self.assertEqual(MODULE.registration_identity(self.root), ("oe-rva23-qemu-201", 24))
        inode = path.stat().st_ino
        path.write_text(json.dumps({**document, "agentId": 25, "agentName": "other"}), encoding="utf-8-sig")
        self.assertEqual(path.stat().st_ino, inode)
        self.assertNotEqual(MODULE.registration_identity(self.root), ("oe-rva23-qemu-201", 24))
        path.write_text(json.dumps({**document, "disableUpdate": False}), encoding="utf-8-sig")
        with self.assertRaises(ValueError):
            MODULE.registration_identity(self.root)
        self.assertIn('(runner / ".runner").read_text(encoding="utf-8-sig")', EMBEDDED)
        self.assertNotIn('(runner / ".credentials").read', EMBEDDED)

    def test_consumed_prepare_is_not_replayed(self):
        state = self.root / "state"
        state.mkdir()
        prepared, _ = self.proof()
        prepared.update(status="payload-installed-stopped", source_fingerprint="reviewed")
        (state / "state.json").write_text(json.dumps(prepared))
        arguments = ["apply", str(self.root), str(self.root / "runner"), str(self.root / "config"),
                     str(self.root / "libexec"), str(self.root / "unit"), str(state),
                     prepared["host"], prepared["name"], prepared["source_commit"], "", "", str(self.root / "receipt")]
        with mock.patch.object(MODULE.os, "geteuid", return_value=0), \
             mock.patch.object(MODULE, "trusted_path"), \
             mock.patch.object(MODULE, "source_fingerprint", return_value="reviewed"), \
             mock.patch.object(MODULE, "replace_payload") as replace, \
             self.assertRaisesRegex(ValueError, "consumed/partial"):
            MODULE.main(arguments)
        replace.assert_not_called()

    def test_cross_device_rejected_before_replacement(self):
        def path(device):
            return types.SimpleNamespace(stat=lambda: types.SimpleNamespace(st_dev=device))
        MODULE.require_same_device([path(1), path(1)])
        with self.assertRaisesRegex(ValueError, "cross filesystems"):
            MODULE.require_same_device([path(1), path(2)])

    def test_installer_failure_restores_complete_contract_and_stays_failed(self):
        runner, staged, backup = self.root / "runner", self.root / "stage", self.root / "backup"
        old_records = self.extract("old", runner)
        new_records = self.extract("new", staged)
        self.preserved(runner)
        (runner / ".release").write_text("old release")
        backup.mkdir(mode=0o700)
        config, libexec, unit, state = [self.root / name for name in ("config", "libexec", "unit", "state")]
        for directory in (config, libexec, state):
            directory.mkdir()
        (config / "policy.conf").write_text("old policy")
        (libexec / "helper.sh").write_text("old helper")
        unit.write_text("old unit")
        with mock.patch.object(MODULE, "trusted_path"):
            MODULE.backup_managed(backup, config, libexec, unit)
        MODULE.replace_payload(runner, staged, backup, new_records)
        (config / "policy.conf").write_text("partial new policy")
        (libexec / "helper.sh").write_text("partial new helper")
        unit.write_text("partial new unit")
        prepared, _ = self.proof()
        prepared.update(status="payload-installed-stopped", source_fingerprint="reviewed", backup=str(backup))
        (state / "state.json").write_text(json.dumps(prepared))
        args = ["rollback", str(self.root), str(runner), str(config), str(libexec), str(unit), str(state),
                prepared["host"], prepared["name"], prepared["source_commit"], "", "", ""]
        with mock.patch.object(MODULE.os, "geteuid", return_value=0), \
             mock.patch.object(MODULE, "trusted_path"), \
             mock.patch.object(MODULE, "source_fingerprint", return_value="reviewed"), \
             mock.patch.object(MODULE, "verify_release"), \
             mock.patch.object(MODULE, "archive_records", return_value=old_records), \
             mock.patch.object(MODULE.subprocess, "run") as process:
            MODULE.main(args)
        self.verify(runner, old_records)
        self.assertEqual((config / "policy.conf").read_text(), "old policy")
        self.assertEqual((libexec / "helper.sh").read_text(), "old helper")
        self.assertEqual(unit.read_text(), "old unit")
        self.assertEqual(json.loads((state / "state.json").read_text())["status"], "failed-restored-old-stopped-needs-review")
        process.assert_not_called()


class UpgradeEntrypointTests(unittest.TestCase):
    def test_shell_replay_refuses_before_service_mutation_or_old_transaction_rollback(self):
        for status in ("applying-stopped", "payload-installed-stopped", "upgraded-stopped-awaiting-activation"):
            with self.subTest(status=status), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                source, commands = root / "source", root / "commands"
                source.mkdir()
                commands.mkdir()
                base = root / "runners"
                (base / ".locks").mkdir(parents=True, mode=0o755)
                states = root / "state"
                state = states / "oe-rva23-qemu-201"
                state.mkdir(parents=True)
                prepared = {"status": status, "host": "10.230.50.201", "name": "oe-rva23-qemu-201",
                            "source_commit": "a" * 40, "source_fingerprint": "reviewed"}
                raw = json.dumps(prepared)
                (state / "state.json").write_text(raw)
                event = root / "events"
                # Use the real shell order and real helper admission/state check;
                # replace only privilege/platform/filesystem-root boundaries.
                script = SOURCE.replace("state_root=/var/lib/openeuler-actions-runner-upgrade", f"state_root={states}")
                script = script.replace('if __name__ == "__main__":',
                                        'trusted_path = lambda *args, **kwargs: None\n'
                                        'source_fingerprint = lambda source: "reviewed"\n'
                                        'os.geteuid = lambda: 0\n'
                                        'if __name__ == "__main__":')
                (source / "upgrade.sh").write_text(script)
                library = f'''set -Eeuo pipefail
oe_runner_base={base}
oe_runner_lock_dir={base}/.locks
oe_runner_config={root}/config
oe_runner_libexec={root}/libexec
oe_die() {{ printf '%s\\n' "$*" >&2; exit 1; }}
oe_usage_error() {{ oe_die "$@"; }}
oe_reject_secret_arguments() {{ :; }}
oe_parse_host_name_args() {{ OE_ARG_HOST=10.230.50.201; OE_ARG_NAME=oe-rva23-qemu-201; OE_ARG_ALLOW_DEGRADED=false; }}
oe_require_root() {{ :; }}
oe_assert_local_host() {{ :; }}
oe_assert_platform() {{ :; }}
oe_rollout_stage() {{ echo canary; }}
oe_load_identity() {{ OE_IDENTITY_HOST=$OE_ARG_HOST; OE_IDENTITY_NAME=$OE_ARG_NAME; OE_IDENTITY_ALLOW_DEGRADED=false; }}
oe_load_policy() {{ :; }}
oe_load_release_lock() {{ :; }}
oe_check_no_other_runners() {{ :; }}
oe_runner_dir() {{ echo {base}/oe-rva23-qemu-201; }}
oe_service_name() {{ echo openeuler-actions-runner@oe-rva23-qemu-201.service; }}
oe_systemctl() {{ echo "SYSTEMCTL $*" >>{event}; return 0; }}
'''
                (source / "_lib.sh").write_text(library)
                for name, body in {"stat": "echo root:root:755", "flock": "exit 0", "install": "exit 0",
                                   "pgrep": f"echo PGREP >>{event}; exit 1",
                                   "docker": f"echo DOCKER >>{event}; exit 0"}.items():
                    executable = commands / name
                    executable.write_text("#!/bin/sh\n" + body + "\n")
                    executable.chmod(0o755)
                (commands / "python3").symlink_to(sys.executable)
                result = subprocess.run(["bash", str(source / "upgrade.sh"), "apply", "--host", "10.230.50.201",
                                         "--name", "oe-rva23-qemu-201", "--source-commit", "a" * 40,
                                         "--github-receipt", str(root / "unused-receipt")],
                                        env={**os.environ, "PATH": str(commands) + os.pathsep + os.environ["PATH"]},
                                        capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("consumed/partial", result.stderr)
                self.assertFalse(event.exists(), result.stdout + result.stderr)
                self.assertEqual((state / "state.json").read_text(), raw)

    def test_help_and_shell_syntax_are_host_read_only(self):
        syntax = subprocess.run(["bash", "-n", str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(syntax.returncode, 0, syntax.stderr)
        help_result = subprocess.run(["bash", str(SCRIPT), "--help"], capture_output=True, text=True)
        self.assertEqual(help_result.returncode, 0, help_result.stderr)
        self.assertIn("STOPPED", help_result.stdout)

    def test_rejects_secret_arguments_before_platform_or_mutation(self):
        result = subprocess.run(["bash", str(SCRIPT), "prepare", "--token", "fixture"], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("credentials are forbidden", result.stderr)

    def test_full_installer_only_after_payload_and_no_registration_or_activation(self):
        self.assertLess(SOURCE.index('payload_operation "$phase"'), SOURCE.index('"$source_dir/install.sh"'))
        self.assertLess(SOURCE.index('oe_assert_platform "$OE_ARG_ALLOW_DEGRADED"'), SOURCE.index('oe_systemctl disable --now "$service"'))
        self.assertIn('payload_operation rollback', SOURCE)
        self.assertIn('prepared["status"] == "prepared-stopped"', SOURCE)
        self.assertIn('containers=$(docker ps --quiet) || oe_die', SOURCE)
        self.assertIn('(prepared["retained"], prepared["name"], prepared["runner_id"])', SOURCE)
        self.assertNotIn('"$source_dir/register.sh"', SOURCE)
        self.assertNotIn('"$source_dir/uninstall.sh"', SOURCE)
        self.assertNotIn('"$source_dir/activate.sh"', SOURCE)
        self.assertNotIn('systemctl start', SOURCE)
        self.assertNotIn('rm -rf', SOURCE)
        self.assertLess(SOURCE.index('"upgrade/backup/managed paths cross filesystems'), SOURCE.index('replace_payload(runner, state / "new-payload"'))


if __name__ == "__main__":
    unittest.main()
