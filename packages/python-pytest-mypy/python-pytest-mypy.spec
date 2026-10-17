# SPDX-License-Identifier: Apache-2.0
Name:           python-pytest-mypy
Version:        1.0.1
Release:        1%{?dist}
Summary:        Mypy static type checker plugin for pytest
License:        MIT
URL:            https://github.com/realpython/pytest-mypy
Source0:        pytest_mypy-1.0.1.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools >= 61
BuildRequires:  python3-setuptools_scm >= 7.1
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
BuildRequires:  python3-filelock >= 3
BuildRequires:  python3-mypy >= 1
BuildRequires:  python3-pytest >= 7
BuildRequires:  python3-packaging
BuildRequires:  python3-pytest-cov
BuildRequires:  python3-pytest-randomly
BuildRequires:  python3-pytest-xdist
BuildRequires:  python3-pexpect
Requires:       python3
Requires:       python3-filelock >= 3
Requires:       python3-mypy >= 1
Requires:       python3-pytest >= 7
Requires:       python3-packaging
Requires:       python3-pytest-cov
Requires:       python3-pytest-randomly
Requires:       python3-pytest-xdist
Requires:       python3-pexpect
BuildArch:      noarch

%description
Pytest-mypy runs the mypy static type checker from pytest. This package retains
the whole original test suite, branch coverage gate, xdist variants and original
upstream skip/xfail markers for source and installed-RPM verification.

%prep
%autosetup -n pytest_mypy-%{version}

%build
export PIP_DISABLE_PIP_VERSION_CHECK=1
python3 -m pip wheel --no-build-isolation --no-deps --no-index --wheel-dir dist .

%install
python3 -m pip install --no-index --no-deps --no-compile --root %{buildroot} --prefix %{_prefix} dist/pytest_mypy-%{version}-py3-none-any.whl
install -d %{buildroot}%{_datadir}/%{name}/source/src/pytest_mypy %{buildroot}%{_datadir}/%{name}/source/tests %{buildroot}%{_datadir}/%{name}/source/.github/workflows
install -m 0644 .gitignore CONTRIBUTING.rst LICENSE README.rst changelog.md pyproject.toml tox.ini %{buildroot}%{_datadir}/%{name}/source/
install -m 0644 src/pytest_mypy/__init__.py src/pytest_mypy/py.typed %{buildroot}%{_datadir}/%{name}/source/src/pytest_mypy/
install -m 0644 tests/conftest.py tests/test_pytest_mypy.py %{buildroot}%{_datadir}/%{name}/source/tests/
install -m 0644 .github/workflows/validation.yml .github/workflows/publication.yml %{buildroot}%{_datadir}/%{name}/source/.github/workflows/

%check
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
# The original src layout must not shadow the built wheel. Both outer pytest
# and pytester subprocesses use the installed buildroot distribution/entry point.
export PYTHONPATH=%{buildroot}%{python3_sitelib}
python3 -c 'import pytest_mypy; assert pytest_mypy.__file__.startswith("%{buildroot}%{python3_sitelib}/pytest_mypy/")'
# Outer CLI verbosity only; never inject options into nested pytester processes.
# Persist running/failing node IDs without changing original tests or gates.
# Non-exiting outer worker stack dump; original subprocess args stay unchanged.
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

%files
%license LICENSE
%doc README.rst CONTRIBUTING.rst changelog.md
%{python3_sitelib}/pytest_mypy/
%{python3_sitelib}/pytest_mypy-*.dist-info/
%{_datadir}/%{name}/

%changelog
* Sun Oct 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.1-1
- Pin official stable source and preserve whole original tests and coverage gate.
