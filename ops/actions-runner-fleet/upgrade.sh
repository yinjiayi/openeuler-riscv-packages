#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail
set +x
umask 077

source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=_lib.sh
source "$source_dir/_lib.sh"

usage() {
  cat <<'EOF'
Usage: upgrade.sh prepare|apply --host 10.230.50.LAST --name oe-rva23-qemu-LAST
       --source-commit FULL_SHA [--allow-degraded]
       [--old-archive /root/verified-old.tar.gz] [--new-archive /root/verified-new.tar.gz]
       [--github-receipt /root/fresh-offline-observation.json]

Only the reviewed 2.336.0 -> 2.338.2 transition is supported. Prepare stops and
disables the exact unit, verifies the entire old official payload and stages
the locked new payload. Apply requires a fresh coordinator GitHub offline/idle
receipt, preserves registration/runtime data, backs up old payload and managed
files, and invokes this archive's COMPLETE install.sh. No registration token is
accepted. Success remains STOPPED: activation/audit and online readback are
separate coordinator gates. Failure never restarts the deprecated old Runner.
EOF
}

# The embedded helper is importable by isolated fixture tests, not an alternate
# live CLI. Production paths and approved release tuples are fixed below.
payload_operation() {
  python3 - "$@" <<'PY_UPGRADE'
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import pwd
import secrets
import shutil
import stat
import subprocess
import sys
import tarfile
import time

OLD_VERSION = "2.336.0"
OLD_SHA = "04cf0be1aff4c3ec3554466c39124ca250e3effd8873bb7e8d68535aa9505d5d"
OLD_SIZE = 226035903
NEW_VERSION = "2.338.2"
NEW_SHA = "baebf204307bac6193480852732f0aba2ae97b6c5597c244f4d5558390147c40"
NEW_SIZE = 228071396
TOPS = {"bin", "externals", "config.sh", "env.sh", "run-helper.cmd.template",
        "run-helper.sh.template", "run.sh", "safe_sleep.sh"}
REPO = "yinjiayi/openeuler-riscv-packages"
RUNTIME = {"_work", "_diag", "_state"}
CONFIGURATION = {".runner", ".credentials", ".credentials_rsaparams", ".service", ".env", ".path", "svc.sh"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def stream_digest(stream):
    result = hashlib.sha256()
    for block in iter(lambda: stream.read(1024 * 1024), b""):
        result.update(block)
    return result.hexdigest()


def trusted_path(path, directory=False, private=False):
    path = Path(path)
    require(path.is_absolute(), "path must be absolute")
    for parent in reversed(path.parents):
        value = parent.lstat()
        require(stat.S_ISDIR(value.st_mode) and value.st_uid == 0 and not value.st_mode & 0o022,
                "path has an untrusted or linked ancestor")
    value = path.lstat()
    expected = stat.S_ISDIR if directory else stat.S_ISREG
    require(expected(value.st_mode) and value.st_uid == 0 and not value.st_mode & 0o022,
            "path type/owner/permissions are unsafe")
    if private:
        require(not value.st_mode & 0o077, "private state is accessible to another account")
    return value


def atomic_json(path, document):
    temporary = path.with_name(path.name + "." + secrets.token_hex(8))
    with temporary.open("x", encoding="utf-8") as stream:
        os.chmod(temporary, 0o600)
        json.dump(document, stream, sort_keys=True, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)
    descriptor = os.open(str(path.parent), os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def assignments(path):
    trusted_path(path)
    result = {}
    for line in path.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        key, value = line.split("=", 1)
        require(key not in result, "duplicate release field")
        result[key] = value
    return result


def release(version, sha, size):
    return {"version": version, "archive": f"actions-runner-linux-x64-{version}.tar.gz",
            "sha256": sha, "size": str(size)}


def verify_release(runner, config, version, sha, size):
    expected = release(version, sha, size)
    require(assignments(runner / ".release") == expected, "installed .release is not the approved old/new release")
    lock = {"RUNNER_" + key.upper(): value for key, value in expected.items()}
    lock["RUNNER_URL"] = f"https://github.com/actions/runner/releases/download/v{version}/{expected['archive']}"
    require(assignments(config / "runner-release.lock") == lock, "installed lock differs from the approved release")


def archive_records(archive, expected_sha, expected_size, expected_tops=TOPS):
    require(archive.stat().st_size == expected_size and digest(archive) == expected_sha,
            "official archive size/SHA-256 mismatch")
    records = {}
    total = 0
    with tarfile.open(archive, "r:gz") as stream:
        for member in stream:
            raw = member.name
            while raw.startswith("./"):
                raw = raw[2:]
            if raw in ("", ".") and member.isdir():
                continue
            path = PurePosixPath(raw)
            require(not path.is_absolute() and ".." not in path.parts and str(path) == raw.rstrip("/")
                    and path.parts[0] in expected_tops and str(path) not in records,
                    "unsafe or duplicate official archive member")
            require(member.isdir() or member.isfile() or member.issym(), "archive special/hardlink member is forbidden")
            require(not member.mode & 0o7000 and member.size >= 0, "archive special permissions/size are forbidden")
            total += member.size
            require(len(records) < 50000 and total <= 2 * 1024**3, "archive expansion exceeds bounded payload")
            records[str(path)] = {"type": "dir" if member.isdir() else "link" if member.issym() else "file",
                                  "mode": member.mode & 0o777, "size": member.size,
                                  "link": member.linkname if member.issym() else None,
                                  "sha256": stream_digest(stream.extractfile(member)) if member.isfile() else None}
    require({PurePosixPath(p).parts[0] for p in records} == expected_tops, "official archive payload roots differ")
    for name, item in records.items():
        for ancestor in PurePosixPath(name).parents:
            if str(ancestor) != ".":
                require(str(ancestor) in records and records[str(ancestor)]["type"] == "dir", "archive parent is missing or linked")
        if item["type"] == "link":
            link = PurePosixPath(item["link"])
            require(not link.is_absolute(), "absolute archive symlink")
            parts = list(PurePosixPath(name).parent.parts)
            for part in link.parts:
                if part == "..":
                    require(len(parts) > 1, "archive symlink escapes its payload root")
                    parts.pop()
                elif part != ".":
                    parts.append(part)
            target = "/".join(parts)
            require(target in records and records[target]["type"] == "file", "archive symlink target is not a contained regular member")
    return records


def extract_payload(archive, destination, records):
    destination.mkdir(mode=0o700)
    # records already passed archive_records(). Create their audited directory
    # tree first so tar member order need not place parents before children.
    for name, item in sorted(records.items(), key=lambda pair: (pair[0].count("/"), pair[0])):
        if item["type"] == "dir":
            target = destination / name
            target.mkdir(mode=item["mode"])
            target.chmod(item["mode"])
    seen = set()
    # Streaming mode must consume each file in physical archive order. Sorting
    # TarInfo objects and seeking back through gzip repeatedly is quadratic.
    with tarfile.open(archive, "r|gz") as stream:
        for member in stream:
            raw = member.name
            while raw.startswith("./"):
                raw = raw[2:]
            if raw in ("", ".") and member.isdir():
                continue
            path = PurePosixPath(raw)
            name = str(path)
            require(path.parts and not path.is_absolute() and ".." not in path.parts
                    and name == raw.rstrip("/") and path.parts[0] in TOPS
                    and name in records and name not in seen,
                    "extraction contains unsafe, unexpected or duplicate member")
            item = records[name]
            kind = "dir" if member.isdir() else "link" if member.issym() else "file" if member.isfile() else "special"
            require(kind == item["type"] and not member.mode & 0o7000
                    and member.mode & 0o777 == item["mode"] and member.size == item["size"]
                    and (member.linkname if member.issym() else None) == item["link"],
                    "extraction member differs from the audited archive")
            seen.add(name)
            if kind == "file":
                target = destination / name
                with stream.extractfile(member) as source, target.open("xb") as output:
                    shutil.copyfileobj(source, output, length=1024 * 1024)
                target.chmod(item["mode"])
    require(seen == set(records), "extraction is missing audited archive members")
    for name, item in records.items():
        if item["type"] == "link":
            (destination / name).symlink_to(item["link"])
    verify_payload(destination, records)


def verify_payload(directory, records, root_uid=0, root_gid=0):
    found = set()
    for top in {PurePosixPath(p).parts[0] for p in records}:
        root = directory / top
        require(root.exists() and not root.is_symlink(), "payload root is missing or linked")
        found.add(top)
        if root.is_dir():
            for current, dirs, files in os.walk(root, followlinks=False):
                for name in dirs + files:
                    found.add(str((Path(current) / name).relative_to(directory)))
    require(found == set(records), "payload contains missing/extra files (mixed version or untrusted modification)")
    for name, expected in records.items():
        path = directory / name
        value = path.lstat()
        require(value.st_uid == root_uid and value.st_gid == root_gid, "payload ownership differs from the trusted archive installation")
        kind = "link" if stat.S_ISLNK(value.st_mode) else "dir" if stat.S_ISDIR(value.st_mode) else "file" if stat.S_ISREG(value.st_mode) else "special"
        require(kind == expected["type"], "payload type mismatch")
        if kind == "link":
            require(os.readlink(path) == expected["link"], "payload symlink mismatch")
        else:
            require(stat.S_IMODE(value.st_mode) == expected["mode"], "payload permission mismatch")
            if kind == "file":
                require(value.st_nlink == 1 and value.st_size == expected["size"] and digest(path) == expected["sha256"], "payload byte/hardlink mismatch")


def preserved_state(runner):
    trusted_path(runner, directory=True)
    names = {p.name for p in runner.iterdir()}
    require(names <= TOPS | RUNTIME | CONFIGURATION | {".release"}, "unknown runner-root entry; review before upgrade")
    require(RUNTIME | {".runner", ".credentials", ".release"} <= names, "registered runner/runtime state is incomplete")
    result = {}
    account = pwd.getpwnam("oegha")
    for name in sorted(names & (RUNTIME | CONFIGURATION)):
        path = runner / name
        value = path.lstat()
        require((stat.S_ISDIR(value.st_mode) if name in RUNTIME else stat.S_ISREG(value.st_mode)) and value.st_nlink >= 1,
                "registered/runtime path is linked or has an unsafe type")
        if name in RUNTIME:
            require((value.st_uid, value.st_gid, stat.S_IMODE(value.st_mode)) == (account.pw_uid, account.pw_gid, 0o700),
                    "runtime ownership/permissions differ from the installed contract")
        elif name != "svc.sh":
            require(value.st_uid == 0 and value.st_gid == account.pw_gid and stat.S_IMODE(value.st_mode) == 0o640
                    and value.st_nlink == 1, "registration configuration ownership/permissions are unsafe")
        # Never open/hash/print credential or runtime contents. Their unchanged
        # inode, owner and permissions are checked across the payload replacement.
        result[name] = [value.st_ino, value.st_uid, value.st_gid, stat.S_IMODE(value.st_mode)]
    name, runner_id = registration_identity(runner)
    return result, name, runner_id


def registration_identity(runner):
    identity = json.loads((runner / ".runner").read_text(encoding="utf-8-sig"))
    require(identity.get("gitHubUrl", "").rstrip("/") == "https://github.com/" + REPO
            and identity.get("workFolder") == "_work" and type(identity.get("agentId")) is int
            and identity["agentId"] > 0 and identity.get("disableUpdate") is True, "registered runner identity/update policy is unsafe")
    require(isinstance(identity.get("agentName"), str), "registered runner name is missing")
    return identity["agentName"], identity["agentId"]


def source_fingerprint(source):
    trusted_path(source, directory=True)
    values = {}
    for path in sorted(source.rglob("*")):
        trusted_path(path, directory=path.is_dir())
        if path.is_file():
            values[str(path.relative_to(source))] = digest(path)
    return hashlib.sha256(json.dumps(values, sort_keys=True).encode()).hexdigest()


def get_archive(path, supplied, version, sha, size):
    if supplied:
        supplied = Path(supplied)
        trusted_path(supplied)
        require(supplied.stat().st_size == size and digest(supplied) == sha, "pre-staged official archive digest/size mismatch")
        shutil.copyfile(supplied, path)
    else:
        url = f"https://github.com/actions/runner/releases/download/v{version}/actions-runner-linux-x64-{version}.tar.gz"
        subprocess.run(["curl", "--fail", "--silent", "--show-error", "--location", "--proto", "=https", "--proto-redir", "=https",
                        "--connect-timeout", "10", "--max-time", "300", "--retry", "2", "--output", str(path), url], check=True)
    path.chmod(0o600)
    return archive_records(path, sha, size)


def verify_observation(proof, prepared, now):
    expected = {"schema_version": 1, "kind": "runner-upgrade-offline-observation", "repository": REPO,
                "host": prepared["host"], "name": prepared["name"], "runner_id": prepared["runner_id"],
                "prepared_nonce": prepared["nonce"], "source_commit": prepared["source_commit"],
                "old_version": OLD_VERSION, "new_version": NEW_VERSION, "new_sha256": NEW_SHA,
                "status": "offline", "busy": False}
    require(set(proof) == set(expected) | {"observed_at"}, "GitHub observation fields differ")
    for key, value in expected.items():
        require(type(proof[key]) is type(value) and proof[key] == value, "GitHub observation identity/status does not match prepare")
    observed = datetime.datetime.fromisoformat(proof["observed_at"].replace("Z", "+00:00"))
    require(observed.tzinfo is not None, "GitHub observation must have timezone")
    stamp = observed.timestamp()
    require(prepared["prepared_at"] <= stamp <= now and now - stamp <= 300, "GitHub observation is stale/future or predates prepare")


def backup_managed(backup, config, libexec, unit):
    for name, path in (("config", config), ("libexec", libexec)):
        trusted_path(path, directory=True)
        for child in path.rglob("*"):
            trusted_path(child, directory=child.is_dir())
        shutil.copytree(path, backup / name, copy_function=shutil.copy2)
    trusted_path(unit)
    shutil.copy2(unit, backup / "unit")


def require_same_device(paths):
    require(len({path.stat().st_dev for path in paths}) == 1,
            "upgrade/backup/managed paths cross filesystems; refuse before any payload rename")


def replace_payload(runner, staged, backup, records):
    (backup / "payload").mkdir(mode=0o700)
    for name in sorted(TOPS):
        path = runner / name
        if path.is_dir():
            shutil.copytree(path, backup / "payload" / name, symlinks=True)
        else:
            shutil.copy2(path, backup / "payload" / name)
    shutil.copy2(runner / ".release", backup / "old.release")
    (backup / "retired").mkdir(mode=0o700)
    for name in sorted(TOPS):
        os.replace(runner / name, backup / "retired" / name)
    for name in sorted(TOPS):
        os.replace(staged / name, runner / name)
    verify_payload(runner, records)
    temporary = runner / (".release-upgrade-" + secrets.token_hex(8))
    temporary.write_text("".join(f"{k}={v}\n" for k, v in release(NEW_VERSION, NEW_SHA, NEW_SIZE).items()))
    temporary.chmod(0o644)
    os.replace(temporary, runner / ".release")


def restore_payload(runner, backup):
    # Move any current roots aside rather than deleting data; the root-private
    # complete backup is immutable recovery input, never the live credential tree.
    failed = backup / ("failed-payload-" + secrets.token_hex(8))
    failed.mkdir(mode=0o700)
    for name in sorted(TOPS):
        path = runner / name
        if path.exists() or path.is_symlink():
            os.replace(path, failed / name)
        original = backup / "payload" / name
        if original.is_dir():
            shutil.copytree(original, path, symlinks=True)
        else:
            shutil.copy2(original, path)
    shutil.copy2(backup / "old.release", runner / ".release")


def main(argv):
    action, source_s, runner_s, config_s, libexec_s, unit_s, state_s, host, name, commit, old, new, receipt = argv
    source, runner, config, libexec, unit, state = map(Path, (source_s, runner_s, config_s, libexec_s, unit_s, state_s))
    require(os.geteuid() == 0, "upgrade helper requires root")
    if action == "prepare":
        require(not state.exists() and not state.is_symlink(), "upgrade state already exists; reconcile before another attempt")
        state.mkdir(mode=0o700)
        fingerprint = source_fingerprint(source)
        verify_release(runner, config, OLD_VERSION, OLD_SHA, OLD_SIZE)
        retained, actual_name, runner_id = preserved_state(runner)
        require(actual_name == name, "registered runner name mismatch")
        require(shutil.disk_usage(state).free >= 3 * 1024**3, "upgrade staging needs at least 3 GiB free")
        old_records = get_archive(state / "old.tar.gz", old, OLD_VERSION, OLD_SHA, OLD_SIZE)
        verify_payload(runner, old_records)
        new_records = get_archive(state / "new.tar.gz", new, NEW_VERSION, NEW_SHA, NEW_SIZE)
        extract_payload(state / "new.tar.gz", state / "new-payload", new_records)
        prepared = {"status": "prepared-stopped", "host": host, "name": name, "runner_id": runner_id,
                    "nonce": secrets.token_hex(32), "prepared_at": time.time(), "source_commit": commit,
                    "source_fingerprint": fingerprint, "retained": retained,
                    "identity_sha256": digest(config / "identity.conf"), "policy_sha256": digest(config / "policy.conf")}
        atomic_json(state / "state.json", prepared)
        print(json.dumps({k: v for k, v in prepared.items() if k not in {"retained"}}, sort_keys=True))
        return
    trusted_path(state, directory=True, private=True)
    trusted_path(state / "state.json", private=True)
    prepared = json.loads((state / "state.json").read_text())
    require((prepared["host"], prepared["name"], prepared["source_commit"]) == (host, name, commit), "prepared host/source identity mismatch")
    require(source_fingerprint(source) == prepared["source_fingerprint"], "reviewed installer archive changed after prepare")
    if action in {"admit", "apply"}:
        require(prepared["status"] == "prepared-stopped", "prepare is consumed/partial; do not replay apply")
        trusted_path(Path(receipt), private=True)
        require(Path(receipt).stat().st_size <= 16384, "GitHub observation exceeds the size limit")
        proof = json.loads(Path(receipt).read_text())
        verify_observation(proof, prepared, time.time())
        require(preserved_state(runner) == (prepared["retained"], prepared["name"], prepared["runner_id"]), "registration/runtime identity changed")
        require(digest(config / "identity.conf") == prepared["identity_sha256"] and digest(config / "policy.conf") == prepared["policy_sha256"], "identity/policy changed after prepare")
        verify_release(runner, config, OLD_VERSION, OLD_SHA, OLD_SIZE)
        if action == "admit":
            # Read-only admission precedes ANY stop/mask/rollback guard in this
            # invocation. A prior partial/consumed transaction is not ours to
            # roll back without a separately reviewed recovery operation.
            return
        old_records = archive_records(state / "old.tar.gz", OLD_SHA, OLD_SIZE)
        new_records = archive_records(state / "new.tar.gz", NEW_SHA, NEW_SIZE)
        verify_payload(runner, old_records)
        verify_payload(state / "new-payload", new_records)
        backup_root = Path("/var/backups/openeuler-actions-runner")
        backup_root.mkdir(mode=0o700, exist_ok=True)
        trusted_path(backup_root, directory=True, private=True)
        backup = backup_root / (name + "-" + secrets.token_hex(16))
        backup.mkdir(mode=0o700)
        require_same_device((backup, runner, state / "new-payload", config, libexec, unit.parent))
        backup_managed(backup, config, libexec, unit)
        # The receipt is rechecked after potentially slow hashing and before
        # any payload mutation; state consumption also prevents proof replay.
        verify_observation(proof, prepared, time.time())
        prepared.update(status="applying-stopped", backup=str(backup))
        atomic_json(state / "state.json", prepared)
        replace_payload(runner, state / "new-payload", backup, new_records)
        prepared["status"] = "payload-installed-stopped"
        atomic_json(state / "state.json", prepared)
    elif action == "finish":
        require(prepared["status"] == "payload-installed-stopped", "upgrade is not ready for final verification")
        verify_release(runner, config, NEW_VERSION, NEW_SHA, NEW_SIZE)
        verify_payload(runner, archive_records(state / "new.tar.gz", NEW_SHA, NEW_SIZE))
        require(preserved_state(runner) == (prepared["retained"], prepared["name"], prepared["runner_id"]), "registration/runtime identity was not preserved")
        require(digest(config / "identity.conf") == prepared["identity_sha256"] and digest(config / "policy.conf") == prepared["policy_sha256"], "installer changed identity/policy")
        managed = ["_lib.sh", "audit.sh", "preflight.sh", "job-guard.sh", "cleanup.sh", "docker-cleanup.py",
                   "job-started.sh", "job-completed.sh", "credential_exec.py"]
        for filename in managed:
            trusted_path(libexec / filename)
            require(digest(libexec / filename) == digest(source / filename), "installed managed helper differs from reviewed source")
        for filename in ("runner-release.lock", "cleanup-image.lock"):
            trusted_path(config / filename)
            require(digest(config / filename) == digest(source / filename), "installed managed lock differs from reviewed source")
        trusted_path(unit)
        require(digest(unit) == digest(source / unit.name), "installed systemd template differs from reviewed source")
        prepared["status"] = "upgraded-stopped-awaiting-activation"
        prepared["finished_at"] = time.time()
        atomic_json(state / "state.json", prepared)
        print(json.dumps({"status": prepared["status"], "backup": prepared["backup"], "runner_version": NEW_VERSION}))
    elif action == "rollback":
        if prepared["status"] not in {"applying-stopped", "payload-installed-stopped"}:
            return
        backup = Path(prepared["backup"])
        trusted_path(backup, directory=True, private=True)
        # Backup may be partial if failure happened while copying old payload,
        # before the first rename. Do not overwrite a valid original with it.
        if (backup / "retired").exists():
            restore_payload(runner, backup)
        for key, target in (("config", config), ("libexec", libexec)):
            moved = backup / ("failed-" + key + "-" + secrets.token_hex(8))
            os.replace(target, moved)
            shutil.copytree(backup / key, target)
        shutil.copy2(backup / "unit", unit)
        verify_release(runner, config, OLD_VERSION, OLD_SHA, OLD_SIZE)
        verify_payload(runner, archive_records(state / "old.tar.gz", OLD_SHA, OLD_SIZE))
        prepared["status"] = "failed-restored-old-stopped-needs-review"
        atomic_json(state / "state.json", prepared)
        print("Upgrade failed; old verified payload/managed files restored, service stays disabled and masked.", file=sys.stderr)
    else:
        raise ValueError("unknown payload operation")


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as error:
        print("runner-upgrade: " + str(error), file=sys.stderr)
        raise SystemExit(1)
PY_UPGRADE
}

oe_reject_secret_arguments "$@"
if [[ ${1-} == -h || ${1-} == --help ]]; then usage; exit 0; fi
phase=${1-}
[[ $phase == prepare || $phase == apply ]] || oe_usage_error 'first argument must be prepare or apply'
shift
source_commit=
github_receipt=
old_archive=
new_archive=
declare -a identity_arguments=()
while (($#)); do
  case $1 in
    --source-commit|--github-receipt|--old-archive|--new-archive)
      (($# >= 2)) || oe_usage_error "$1 requires a value"
      case $1 in
        --source-commit) source_commit=$2 ;;
        --github-receipt) github_receipt=$2 ;;
        --old-archive) old_archive=$2 ;;
        --new-archive) new_archive=$2 ;;
      esac
      shift 2 ;;
    *) identity_arguments+=("$1"); shift ;;
  esac
done
if ! oe_parse_host_name_args "${identity_arguments[@]}"; then usage; exit 0; fi
[[ $source_commit =~ ^[0-9a-f]{40}$ ]] || oe_usage_error '--source-commit requires the reviewed protected-main archive SHA'
[[ $phase != apply || -n $github_receipt ]] || oe_usage_error 'apply requires --github-receipt'
oe_require_root
oe_assert_local_host "$OE_ARG_HOST"
stage=$(oe_rollout_stage "$OE_ARG_HOST")
if [[ $OE_ARG_ALLOW_DEGRADED == true && $stage != conditional ]]; then
  oe_usage_error '--allow-degraded is restricted to the four audited conditional hosts'
fi
oe_assert_platform "$OE_ARG_ALLOW_DEGRADED"
oe_load_identity
[[ $OE_IDENTITY_HOST == "$OE_ARG_HOST" && $OE_IDENTITY_NAME == "$OE_ARG_NAME" \
  && $OE_IDENTITY_ALLOW_DEGRADED == "$OE_ARG_ALLOW_DEGRADED" ]] || oe_die 'installed identity/degraded flag differs'
oe_load_policy
oe_load_release_lock "$source_dir/runner-release.lock"
oe_check_no_other_runners "$OE_ARG_NAME"
runner_dir=$(oe_runner_dir "$OE_ARG_NAME")
service=$(oe_service_name "$OE_ARG_NAME")
state_root=/var/lib/openeuler-actions-runner-upgrade
[[ ! -L $state_root ]] || oe_die 'upgrade state root must not be linked'
install -d -o root -g root -m 0700 "$state_root"
state_dir=$state_root/$OE_ARG_NAME
if [[ $phase == prepare && ( -e $state_dir || -L $state_dir ) ]]; then
  oe_die 'upgrade state already exists; reconcile before another prepare'
fi
[[ -d $oe_runner_lock_dir && ! -L $oe_runner_lock_dir \
  && $(stat -c '%U:%G:%a' "$oe_runner_lock_dir") == root:root:755 ]] || oe_die 'upgrade lock parent is unsafe'
upgrade_lock=$oe_runner_lock_dir/$OE_ARG_NAME.upgrade.lock
if [[ -e $upgrade_lock || -L $upgrade_lock ]]; then
  [[ -f $upgrade_lock && ! -L $upgrade_lock && $(stat -c '%U:%G:%a' "$upgrade_lock") == root:root:600 ]] || oe_die 'upgrade lock is unsafe'
fi
exec 9>"$upgrade_lock"
flock --nonblock 9 || oe_die 'another upgrade owns this host'

absent_process() {
  local status=0
  pgrep -x "$1" >/dev/null || status=$?
  [[ $status == 1 ]] || oe_die "process inventory failed or $1 is present"
}
quiescent() {
  local containers
  absent_process Runner.Worker
  containers=$(docker ps --quiet) || oe_die 'Docker container inventory failed'
  [[ -z $containers ]] || oe_die 'running containers prevent upgrade'
  if [[ ${1-} == stopped ]]; then
    absent_process Runner.Listener
    [[ $(oe_systemctl show --property=ActiveState --value "$service") == inactive ]] || oe_die 'Runner unit is not inactive'
  fi
}

declare -a helper_arguments=("$source_dir" "$runner_dir" "$oe_runner_config" "$oe_runner_libexec" \
  /etc/systemd/system/openeuler-actions-runner@.service "$state_dir" "$OE_ARG_HOST" "$OE_ARG_NAME" \
  "$source_commit" "$old_archive" "$new_archive" "$github_receipt")
if [[ $phase == apply ]]; then
  payload_operation admit "${helper_arguments[@]}"
  # A prepared host must still be stopped. Do not stop a restarted host and
  # thereby paper over drift since the coordinator's offline observation.
  quiescent stopped
else
  quiescent
fi
# Only this admitted attempt may stop the service or arm rollback below.
oe_systemctl disable --now "$service"
oe_systemctl mask --runtime "$service"
quiescent stopped
completed=false
on_exit() {
  local status=$?
  if [[ $completed == false ]]; then
    set +e
    oe_systemctl disable --now "$service" >/dev/null 2>&1
    oe_systemctl mask --runtime "$service" >/dev/null 2>&1
    if [[ $phase == apply && -f $state_dir/state.json ]]; then
      quiescent stopped
      payload_operation rollback "${helper_arguments[@]}" \
        || printf 'CRITICAL: rollback incomplete; retain stopped host, state and backup for reviewed recovery.\n' >&2
      oe_systemctl daemon-reload >/dev/null 2>&1
    fi
    printf 'Upgrade did not complete. Runner remains disabled/stopped; do not restart old deprecated payload.\n' >&2
  fi
  exit "$status"
}
trap on_exit EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

payload_operation "$phase" "${helper_arguments[@]}"
if [[ $phase == apply ]]; then
  quiescent stopped
  "$source_dir/install.sh" "${identity_arguments[@]}"
  quiescent stopped
  payload_operation finish "${helper_arguments[@]}"
  oe_systemctl unmask --runtime "$service"
  quiescent stopped
fi
completed=true
printf 'Upgrade %s complete for %s; state=%s/state.json. Runner remains stopped.\n' "$phase" "$OE_ARG_NAME" "$state_dir"
