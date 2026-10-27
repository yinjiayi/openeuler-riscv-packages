#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python-pytest-mypy python3-filelock python3-mypy python3-pytest python3-packaging python3-pytest-cov python3-pytest-randomly python3-pytest-xdist python3-pexpect
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONPATH
scratch=$(mktemp -d)
trap 'rm -rf -- "$scratch"' EXIT
cd "$scratch"
python3 - <<'PY'
import ast
import hashlib
import importlib.metadata
from pathlib import Path
import subprocess
import pytest_mypy

assert importlib.metadata.version('pytest-mypy') == '1.0.1'
module = Path(pytest_mypy.__file__).resolve()
assert str(module).startswith('/usr/lib/') and module.parent.name == 'pytest_mypy'
assert subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}', str(module)], text=True) == 'python-pytest-mypy'
owned = Path('/usr/share/python-pytest-mypy/source')
expected = {
    '.github/workflows/publication.yml': 'f8f640cd08f2110b6c240fcf9543e1319f9df8557f21206115fffe5378e1dedb',
    '.github/workflows/validation.yml': '941a11e36a6eac2b023e5ecbda1bc8525fc60be71bdf68adeff217edf9cc1d82',
    '.gitignore': '0871634f97cc5f6890fd1de607559922d3f9ff52ac59784cc682549782168407',
    'CONTRIBUTING.rst': 'e936c4ea05d11d122d8f714cee195c24a633a1c295262522b608797db64f408e',
    'LICENSE': 'fa795384c183b89a4a9a5ba08fa67286eebeb61ad1adfff18d45aa6bc5d896ee',
    'README.rst': '6f1e5a91967bfc98f5fd691b5640e82745e9115aa774271a804cf8e8aa597f63',
    'changelog.md': '85a53a17e1af51df6a1f0f5f23c7a9e6f693cd8acc9425e183ca49e813d7e99f',
    'pyproject.toml': 'f1499c23c68d2d326422b2eba796acfe0fc4542a5c2c58279af43c39d0984deb',
    'src/pytest_mypy/__init__.py': '4a64a8335afa6a2a4d9f081563b0b2ec3d431d0c257cd37ffccb9d0094085ed5',
    'src/pytest_mypy/py.typed': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
    'tests/conftest.py': '26b82604ca34a6a88222d1e63f2f0e72664c170589b214d03ebd867aa1228c8b',
    'tests/test_pytest_mypy.py': '62b258d494bb49d031816a551ab35e2a76d5e1aa06cd48c4633ab92be940ada6',
    'tox.ini': '4c2b6f29d26aaed73b3dfe998159334ebf2e986f80264dfc4c84d07b2625fbe4',
}
actual = {}
for path in sorted(owned.rglob('*')):
    assert not path.is_symlink()
    if path.is_file():
        assert subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}', str(path)], text=True) == 'python-pytest-mypy'
        actual[str(path.relative_to(owned))] = hashlib.sha256(path.read_bytes()).hexdigest()
assert actual == expected
assert module.read_bytes() == (owned / 'src/pytest_mypy/__init__.py').read_bytes()
assert sum(isinstance(node, ast.FunctionDef) and node.name.startswith('test_') for node in ast.walk(ast.parse((owned / 'tests/test_pytest_mypy.py').read_bytes()))) == 29
ep = [e for e in importlib.metadata.distribution('pytest-mypy').entry_points if e.group == 'pytest11' and e.name == 'mypy']
assert len(ep) == 1 and ep[0].value == 'pytest_mypy'
print('Installed RPM-owned pytest-mypy 1.0.1, exact original 13 files and all 29 test functions verified; original skip/xfail retained')
PY
cp -R /usr/share/python-pytest-mypy/source/tests "$scratch/tests"
cp /usr/share/python-pytest-mypy/source/tox.ini "$scratch/tox.ini"
test ! -e "$scratch/pytest_mypy"
test ! -e "$scratch/src"
# Outer CLI verbosity only, matching source %check; nested pytester is unchanged.
# Retain whole original tests, xdist, branch coverage and existing deadlines.
# Non-exiting outer worker stack dump, not a test timeout or nested option.
# Flush complete failed reports from the outer controller before the deadline.
# The explicit plugin object is not exported to workers or pytester children.
python3 - -p no:mypy --cov pytest_mypy --cov-branch --cov-fail-under 100 --cov-report term-missing -n auto -vv -rA -o faulthandler_timeout=300 <<'OE_REPORT_PY'
import datetime
import json
import os
import sys
import pytest

# BEGIN packaging-only child observer
import hashlib
import json
import os
from pathlib import Path
import stat
import threading
import time


def process_stat(raw):
    """Read only Linux stat's PID, parent, state, CPU ticks and start identity."""
    left = raw.index(" (")
    right = raw.rindex(") ")
    pid = int(raw[:left])
    fields = raw[right + 2:].split()
    if pid <= 0 or len(fields) < 20 or fields[0] not in "RSDZTWtXxKWPIN":
        raise ValueError("invalid process stat")
    values = [int(fields[index]) for index in (1, 11, 12, 19)]
    if any(value < 0 for value in values):
        raise ValueError("negative process stat")
    return dict(pid=pid, ppid=values[0], state=fields[0],
                user_ticks=values[1], system_ticks=values[2], start_ticks=values[3])


def output_tail(cwd, root, name, limit=2048):
    """Read a fixed pytester output file, never an arbitrary or symlinked file."""
    if name not in ("stdout", "stderr") or not 1 <= limit <= 2048:
        raise ValueError("invalid output request")
    relative = cwd.relative_to(root)
    if not relative.parts or any(part in ("", ".", "..") for part in relative.parts):
        raise ValueError("invalid output directory")
    if not any(part.startswith("pytest-") for part in relative.parts):
        return None
    descriptors = []
    try:
        directory = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        descriptors.append(directory)
        for part in relative.parts:
            directory = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                dir_fd=directory)
            descriptors.append(directory)
        descriptor = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                             dir_fd=directory)
        descriptors.append(descriptor)
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode):
            raise ValueError("output is not regular")
        os.lseek(descriptor, max(0, info.st_size - limit), os.SEEK_SET)
        data = os.read(descriptor, limit)
        return dict(directory=str(relative), name=name, bytes=info.st_size,
                    tail_bytes=len(data), tail_sha256=hashlib.sha256(data).hexdigest(),
                    tail=data.decode("utf-8", errors="replace"))
    finally:
        for descriptor in reversed(descriptors):
            os.close(descriptor)


def child_snapshot(proc_root, temp_root, owner, limit=64):
    """Snapshot only descendants of this controller; no environment or argv."""
    proc_root, temp_root = Path(proc_root), Path(temp_root)
    processes, errors = {}, {}
    for entry in sorted(proc_root.iterdir(), key=lambda path: path.name):
        if not entry.name.isascii() or not entry.name.isdecimal():
            continue
        try:
            item = process_stat((entry / "stat").read_text(encoding="ascii"))
            if item["pid"] != int(entry.name):
                raise ValueError("process identity mismatch")
            processes[item["pid"]] = item
        except (OSError, ValueError, UnicodeError) as error:
            key = type(error).__name__
            errors[key] = errors.get(key, 0) + 1
    if owner not in processes:
        raise ValueError("observer owner missing")
    descendants = {owner}
    while True:
        added = {pid for pid, item in processes.items()
                 if item["ppid"] in descendants and pid not in descendants}
        if not added:
            break
        descendants.update(added)
    selected = sorted(descendants - {owner})
    records = []
    for pid in selected[:limit]:
        item = dict(processes[pid])
        item["outputs"] = []
        try:
            # Guard PID reuse between the tree snapshot and path observation.
            current = process_stat((proc_root / str(pid) / "stat").read_text(encoding="ascii"))
            if current["start_ticks"] != item["start_ticks"]:
                raise ValueError("process identity changed")
            cwd = Path(os.readlink(proc_root / str(pid) / "cwd"))
            if cwd.is_absolute() and cwd.is_relative_to(temp_root):
                for name in ("stdout", "stderr"):
                    try:
                        result = output_tail(cwd, temp_root, name)
                        if result is not None:
                            item["outputs"].append(result)
                    except (OSError, ValueError) as error:
                        item.setdefault("output_errors", {})[name] = type(error).__name__
        except (OSError, ValueError, UnicodeError) as error:
            item["observation_error"] = type(error).__name__
        records.append(item)
    return dict(processes=records, descendant_count=len(selected),
                truncated=len(selected) > limit, stat_read_errors=errors)


class SerializedStream:
    """Serialize complete records from the controller and observer thread."""
    def __init__(self, stream):
        self.stream = stream
        self.lock = threading.Lock()

    def write(self, value):
        with self.lock:
            return self.stream.write(value)

    def flush(self):
        with self.lock:
            return self.stream.flush()


class ChildObserver:
    """A controller-only daemon; no test/process timeout or child injection."""
    def __init__(self, stream, proc_root="/proc", temp_root="/tmp", interval=60):
        self.stream = stream
        self.proc_root = Path(proc_root)
        self.temp_root = Path(temp_root).resolve()
        self.owner = os.getpid()
        self.interval = interval
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.observe, daemon=True)

    def observe(self):
        while not self.stop_event.wait(self.interval):
            try:
                record = child_snapshot(self.proc_root, self.temp_root, self.owner)
                record["monotonic_seconds"] = time.monotonic()
            except (OSError, ValueError, UnicodeError) as error:
                record = {"observer_error": type(error).__name__}
            self.stream.write("OE_PYTEST_CHILD_SNAPSHOT " + json.dumps(record, ensure_ascii=True) + "\n")
            self.stream.flush()

    def start(self):
        self.thread.start()

    def close(self):
        self.stop_event.set()
        self.thread.join(timeout=1)
# END packaging-only child observer

class ImmediateFailureReporter:
    def __init__(self, stream):
        self.stream = stream

    def pytest_runtest_logreport(self, report):
        if not report.failed:
            return
        record = {
            "at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "nodeid": report.nodeid,
            "when": report.when,
            "outcome": report.outcome,
            "duration": report.duration,
            "longreprtext": report.longreprtext,
            "sections": list(report.sections),
        }
        self.stream.write("OE_PYTEST_FAILURE_REPORT " + json.dumps(record, ensure_ascii=True) + "\n")
        self.stream.flush()

def main():
    descriptor = os.dup(2)
    os.set_inheritable(descriptor, False)
    with os.fdopen(descriptor, "w", encoding="utf-8", errors="backslashreplace") as stream:
        stream = SerializedStream(stream)
        observer = ChildObserver(stream)
        observer.start()
        try:
            return int(pytest.main(sys.argv[1:], plugins=[ImmediateFailureReporter(stream)]))
        finally:
            observer.close()

if __name__ == "__main__":
    raise SystemExit(main())
OE_REPORT_PY
