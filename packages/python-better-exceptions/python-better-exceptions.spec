# SPDX-License-Identifier: Apache-2.0
Name:           python-better-exceptions
Version:        0.4.0
Release:        2%{?dist}
Summary:        Pretty and helpful Python exceptions
License:        MIT AND Python-2.0
URL:            https://github.com/Qix-/better-exceptions
Source0:        python-better-exceptions-0.4.0.tar.gz
Source1:        PYTHON-LICENSE.txt
Source2:        PYTEST-COV-MIT-LICENSE.txt
Source3:        PYTEST-COV-AUTHORS.rst
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-unversioned-command
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  /usr/bin/bash
BuildRequires:  /usr/bin/env
BuildRequires:  /usr/bin/sed
BuildRequires:  /usr/bin/grep
BuildRequires:  /usr/bin/diff
BuildRequires:  /usr/bin/cat
BuildRequires:  /usr/bin/expect
BuildRequires:  /usr/bin/ps
BuildRequires:  /usr/bin/python3
BuildRequires:  /usr/lib64/python3.11/lib-dynload/_curses.cpython-311-riscv64-linux-gnu.so
BuildRequires:  /usr/share/terminfo/x/xterm
BuildRequires:  /usr/share/terminfo/v/vt100
BuildRequires:  /usr/share/terminfo/d/dumb
BuildRequires:  /usr/lib/python3.11/site-packages/setuptools/command/develop.py
BuildRequires:  /usr/lib/python3.11/site-packages/setuptools/command/easy_install.py
BuildRequires:  /usr/lib/python3.11/site-packages/setuptools/command/install_lib.py
BuildRequires:  /usr/lib/python3.11/site-packages/setuptools/_distutils/command/build.py
BuildRequires:  /usr/lib/python3.11/site-packages/setuptools/_distutils/core.py
BuildRequires:  /usr/bin/python
BuildRequires:  /usr/bin/mkdir
Requires:       python3
Requires:       python3-setuptools
Requires:       python3-unversioned-command
Requires:       /usr/bin/bash
Requires:       /usr/bin/env
Requires:       /usr/bin/sed
Requires:       /usr/bin/grep
Requires:       /usr/bin/diff
Requires:       /usr/bin/cat
Requires:       /usr/bin/expect
Requires:       /usr/bin/ps
Requires:       /usr/bin/python3
Requires:       /usr/lib64/python3.11/lib-dynload/_curses.cpython-311-riscv64-linux-gnu.so
Requires:       /usr/share/terminfo/x/xterm
Requires:       /usr/share/terminfo/v/vt100
Requires:       /usr/share/terminfo/d/dumb
Requires:       /usr/lib/python3.11/site-packages/setuptools/command/develop.py
Requires:       /usr/lib/python3.11/site-packages/setuptools/command/easy_install.py
Requires:       /usr/lib/python3.11/site-packages/setuptools/command/install_lib.py
Requires:       /usr/lib/python3.11/site-packages/setuptools/_distutils/command/build.py
Requires:       /usr/lib/python3.11/site-packages/setuptools/_distutils/core.py
Requires:       /usr/bin/python
Requires:       /usr/bin/mkdir

%description
Pretty Python exception formatting and an opt-in startup hook, with unchanged
original terminal golden tests and complete original/copy-derived notices.

%prep
%setup -q -n better-exceptions-8fa00a74cf2a43e5f7012f158f0e16ea6216eaa0
mkdir -p ../better-pristine
cp -a . ../better-pristine/
cp -p %{SOURCE1} PYTHON-LICENSE.txt
cp -p %{SOURCE2} PYTEST-COV-MIT-LICENSE.txt
cp -p %{SOURCE3} PYTEST-COV-AUTHORS.rst
cat > BETTER-ATTRIBUTION.txt <<'NOTICE'
Better-exceptions 0.4.0 attribution and derivative changes

All 47 original files are retained byte-for-byte from official fixed commit
8fa00a74cf2a43e5f7012f158f0e16ea6216eaa0. Original MIT license copyright
2016 Josh Junon and runtime copyright 2017 Josh Junon remain unchanged.

The setup.py comment identifies copied PTH command classes from pytest-cov
cde7c378b6a1971957759f42ac91e2860b41cf89/setup.py. Preserve its complete MIT
license copyright 2010 Meme Dough and complete AUTHORS.rst. The four class
bodies match normalized AST after replacing src/pytest-cov.pth with
better_exceptions_hook.pth; no unique first-copy date is asserted.
Primary source: https://github.com/pytest-dev/pytest-cov/blob/cde7c378b6a1971957759f42ac91e2860b41cf89/setup.py

better_exceptions/formatter.py cites CPython traceback.py fixed commit
a5b76167dedf4d15211a216c3ca7b98e3cec33b8. Preserve the complete historical
Python license chain including PSF, BeOpen, CNRI and CWI copyrights/history.
The adapted cause/context exception chaining and formatting logic is combined
with Better's recursive formatter, colored locals, Unicode output and assertion
presentation. It is not byte-identical code or a unique-copy-version claim.
Primary source: https://github.com/python/cpython/blob/a5b76167dedf4d15211a216c3ca7b98e3cec33b8/Lib/traceback.py#L468

Aggregate source attribution is MIT AND Python-2.0, not a universal MIT-only
claim. Full PYTHON-LICENSE.txt and PYTEST-COV-MIT-LICENSE.txt are included,
alongside original LICENSE.txt and contributor list. Recipe/runner helpers
are Apache-2.0 separately. No endorsement by original authors is implied.
NOTICE

%build
SOURCE_DATE_EPOCH=315532800 %{__python3} -m pip wheel --no-deps --no-index --no-build-isolation --wheel-dir wheelhouse .

%install
%{__python3} -m pip install --no-deps --no-index --no-compile --root %{buildroot} --prefix %{_prefix} wheelhouse/better_exceptions-0.4.0-*.whl
install -d %{buildroot}%{_datadir}/python-better-exceptions/original
cp -a ../better-pristine/. %{buildroot}%{_datadir}/python-better-exceptions/original/
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/python-better-exceptions/python-better-exceptions-0.4.0.tar.gz
install -m 0644 PYTHON-LICENSE.txt PYTEST-COV-MIT-LICENSE.txt PYTEST-COV-AUTHORS.rst BETTER-ATTRIBUTION.txt %{buildroot}%{_datadir}/python-better-exceptions/
cat > %{buildroot}%{_datadir}/python-better-exceptions/original-files.json <<'JSON'
{".editorconfig": "ec50d8ab317928b0fa93e5ca3812def731c044a3ad05e07f4db93763d2aa238b", ".github/FUNDING.yml": "a9cb0a37d3604fdc765dd781cfefe2973eafb2ebf536c14b4e8c43f5cd5647f1", ".github/workflows/push.yml": "608c602cf02a139e1eae5e714a32d4f4f5fe8e3eeae77778b0edcc0bf0a4a6f9", ".gitignore": "6b2a9be7123008f5fdcfe0f5d48a51de70c2d0bf4d5057617a59761b805c9ca3", "LICENSE.txt": "d941ab46ceb5e77d7a3caa2795d14e507047d6abdf59a4e6b95e026b5b366ad7", "MANIFEST.in": "f2a67207318ae699d90677b3b58f50be66c236ca182735a4c99a24685f87402b", "README.md": "38f3396dc63856e063ae42ea22a4189c89f53f3d2bdcae7c3f0c45c594a0fd5f", "better_exceptions/__init__.py": "8eb87711be0d27f063edd4cd4c714e70a4e0ec0ff655f915da4e131dbcfc8c67", "better_exceptions/__main__.py": "4e25eba25986769ebe50979047f1448d3d1fd0ee255210bc6ab7df55b1d9b321", "better_exceptions/color.py": "e2ebbf140021c842a531a69504315f738cf47eb208af940e91c4550b8e28d62e", "better_exceptions/formatter.py": "b43bc82f3b5bc95dc3341801bd5d29184c4f54f30de41cc15d75d5ab986902a8", "better_exceptions/integrations/__init__.py": "01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b", "better_exceptions/integrations/django.py": "d7fcc6f2b3a9b24dbee13a95d8b15b6798207d31a125bba58330078fa2ef4f13", "better_exceptions/log.py": "391348d813ebf027992d2150a3f816f855786c4a385a5ceb7aa7ca82bde670e6", "better_exceptions/repl.py": "aefd7243041fbdf9e71cfec0799ac57388a17f646e2760becf2c86c011fd1a6f", "better_exceptions_hook.pth": "3785c2ed5d41adf57fd7d3584ef639b01c03c83048267321453b335ea5d60083", "screenshot.png": "9d3aed0cb98ac8bb9bdf802271c3b5c4b11a4d1140b5fae457cc288dc9e732ae", "setup.cfg": "d4ef8a1566ce43a6411113cbcfeb425255e23942b4e126f598aaa8f812dd035c", "setup.py": "81c87b148562b6c1e05fe1d659e534ebb57cbd6c494bacddf6f21eb84630f8e6", "test/output/python3-dumb-UTF-8-color.out": "c85cf25e1187bc79aeee579f07f80c1df56366cff8f47c1b4183d4cb8c3b00a4", "test/output/python3-dumb-UTF-8-nocolor.out": "4ceba9e75b7e60c3a79bd47909683960d8c5a602a02d6809544b21670ac7140c", "test/output/python3-dumb-ascii-color.out": "ee736aa63b5753259f41756d39d4c74ec4fc6085f29f8d3758ce7cf15113c0b3", "test/output/python3-dumb-ascii-nocolor.out": "04f23d65fbf37bbd87653cac5280ca99196e9fc0bbeacac7327a1b043cac5823", "test/output/python3-vt100-UTF-8-color.out": "c85cf25e1187bc79aeee579f07f80c1df56366cff8f47c1b4183d4cb8c3b00a4", "test/output/python3-vt100-UTF-8-nocolor.out": "4ceba9e75b7e60c3a79bd47909683960d8c5a602a02d6809544b21670ac7140c", "test/output/python3-vt100-ascii-color.out": "ee736aa63b5753259f41756d39d4c74ec4fc6085f29f8d3758ce7cf15113c0b3", "test/output/python3-vt100-ascii-nocolor.out": "04f23d65fbf37bbd87653cac5280ca99196e9fc0bbeacac7327a1b043cac5823", "test/output/python3-xterm-UTF-8-color.out": "c85cf25e1187bc79aeee579f07f80c1df56366cff8f47c1b4183d4cb8c3b00a4", "test/output/python3-xterm-UTF-8-nocolor.out": "c1ee42de7bb71df2637a72a22c316dd6817c2e8237b138797dee4a43f9af2445", "test/output/python3-xterm-ascii-color.out": "ee736aa63b5753259f41756d39d4c74ec4fc6085f29f8d3758ce7cf15113c0b3", "test/output/python3-xterm-ascii-nocolor.out": "0b2eab3f3cbb28ea1a4a3f48207dd536de7b83e5fb3f37ac668a7ae909712c85", "test/test.py": "1ed1c4085450ae3d4f96d15ca67d4733968ea54b8568ccaad845886a79c20a45", "test/test_chaining.py": "123c420260f30438be32bb58b2faf678f638fdbd1029e0bf4a804d2d437fae39", "test/test_color.py": "3769e222479cbaf9fc0e6f9f36116ca0dbdb725aec1d37b8a246c3bf7a9d95c4", "test/test_encoding.py": "929d389e054c2d575f428f40da820c4e1486c597286d87de00f2692b29ee7aad", "test/test_indentation_error.py": "d11586556a2d572ba8973c190c46ae2e072630ea342f0a6241ae6ac44085801b", "test/test_interactive.sh": "a838163dbd80c79bb36184670f2381b0d6ff49c269d880863dd04a81191b6c78", "test/test_interactive_raw.sh": "7a7e3c10470dc5454b78f923ce8431f6a17fd937443de2b21b8dcc92621716aa", "test/test_logging.py": "3dc2804e88d65ae019dd3298631232d6555fdaf491794ebacc9136611db8a4c6", "test/test_string.sh": "3d9ca4dafb666b9cefe775497108a0558b039fa8042a3649683391787e20f92d", "test/test_syntax_error.py": "be67f93de7ce883d28719401521a8ab2622be2bd002d559e6b0b250951e2bb81", "test/test_truncating.py": "3ef9a40a96fb7196bf51a81ef4e85e3881b93ca31d5ab82842ad0338a699ac38", "test/test_truncating_disabled.py": "d28cc6f554f4ec83be25ee502bffa7de4c03a390451e4df12a755ae55d3871a7", "test/test_unittest_patch.py": "9e9681ea58b0da9e472497cd0b8164d53cd2f3a55ddde08599e70fc58788f612", "test/test_util/__init__.py": "cd915d1088dc8e6fa978b2d00263a36542b43737c1bbf94d4f48f4f47f3c650c", "test/test_util/quiet_console.py": "938ddb0ee1b0bbdfe68dcfed36affaa40aa77ff3670cb24589ff29b7548db8b5", "test_all.sh": "50bb6b49607bf456fdf0c7220436d0a139ae19ad40d771b21a2c658b385f5bd6"}
JSON
cat > %{buildroot}%{_datadir}/python-better-exceptions/legal-files.json <<'JSON'
{"BETTER-ATTRIBUTION.txt": "d2a26ca3e9f20df31a506cce5aae25b2f9928eacb925f954ed0dfd5fb4b9f47b", "PYTEST-COV-AUTHORS.rst": "e7d3fd5b8c1def57317a8a68b54b1cb3d93829767e6fa6e8d719f3b0069f7523", "PYTEST-COV-MIT-LICENSE.txt": "835586ae156766a24e3c103fbc55d9af6b1a16df57ca932c97482a2737fd83d5", "PYTHON-LICENSE.txt": "a77d71d6be6f9032e6b6e5d2cf6da68f9eeab9036edfbc043633c8979cd5e82c"}
JSON

%check
env -u BETTER_EXCEPTIONS -u PYTHONHOME -u PYTHONSTARTUP -u PYTHONPATH %{__python3} - "%{buildroot}%{_datadir}/python-better-exceptions/original" "%{buildroot}%{python3_sitelib}" buildroot <<'PY'
# SPDX-License-Identifier: Apache-2.0
# Target-only proposal. Never execute this runner on the local evidence host.
import hashlib, importlib.metadata, json, os, pathlib, re, shutil, subprocess, sys, tempfile

original = pathlib.Path(sys.argv[1]).resolve()
site = pathlib.Path(sys.argv[2]).resolve()
installed = sys.argv[3] == 'installed'
package = 'python-better-exceptions'
manifest = json.loads((original.parent / 'original-files.json').read_text())
runtime = {p: h for p, h in manifest.items() if p.startswith('better_exceptions/') and p.endswith('.py')}
pth = 'better_exceptions_hook.pth'
runtime[pth] = manifest[pth]
assert len(manifest) == 47 and len(runtime) == 9 and sys.version_info[:2] == (3, 11)

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def owned(p):
    if installed:
        assert subprocess.check_output(['rpm', '-qf', '--qf', '%%{NAME}', str(p)], text=True) == package

def pristine():
    for p, h in manifest.items():
        q = original / p
        assert q.is_file() and not q.is_symlink() and digest(q) == h
        owned(q)
    for p, h in runtime.items():
        q = site / p
        assert q.is_file() and not q.is_symlink() and digest(q) == h
        owned(q)
    for q in (site / 'better_exceptions').rglob('*'):
        if not q.is_file():
            continue
        rel = q.relative_to(site).as_posix()
        if rel not in runtime:
            assert q.parent.name == '__pycache__' and q.suffix == '.pyc' and any(
                p.endswith('.py') and q.parent.parent == site / pathlib.Path(p).parent
                and q.name.startswith(pathlib.Path(p).stem + '.') for p in runtime)
        owned(q)
    owned(original.parent / 'original-files.json')
    for filename, expected in json.loads((original.parent / 'legal-files.json').read_text()).items():
        q = original.parent / filename
        assert q.is_file() and not q.is_symlink() and digest(q) == expected
        owned(q)

pristine()
archive = original.parent / 'python-better-exceptions-0.4.0.tar.gz'
assert digest(archive) == '4237a29497b5b6f1e1df75396bba536c8f2ee950c996e23cb27a90b0129a8e12'
owned(archive)
executable = pathlib.Path(sys.executable).resolve()
os.environ['PATH'] = '/usr/bin:/bin'
for name in ('python', 'python3'):
    command = pathlib.Path('/usr/bin') / name
    assert command.is_file() and command.resolve() == executable
    assert subprocess.check_output(['rpm', '-qf', '--qf', '%%{NAME}', str(command)], text=True).strip()
assert subprocess.check_output(['rpm', '-qf', '--qf', '%%{NAME}', str(executable)], text=True).strip()
for command in ('bash', 'diff', 'sed', 'grep', 'cat', 'mkdir', 'env', 'ps'):
    tool = shutil.which(command)
    assert tool and pathlib.Path(tool).is_file()
    assert subprocess.check_output(['rpm', '-qf', '--qf', '%%{NAME}', tool], text=True).strip()
assert pathlib.Path('/usr/bin/expect').is_file()
assert subprocess.check_output(['rpm', '-qf', '--qf', '%%{NAME}', '/usr/bin/expect'], text=True).strip()

with tempfile.TemporaryDirectory(prefix='be-', dir='/tmp') as scratch:
    base = pathlib.Path(scratch)
    # Short import path preserves the original module-repr golden normalization:
    # the formatter truncates at 128 characters before test_all.sh runs sed.
    alias = base / 'site'
    alias.symlink_to(site, target_is_directory=True)
    assert alias.is_symlink() and alias.resolve() == site
    assert len("<module 'better_exceptions' from '" + str(alias / 'better_exceptions/__init__.py') + "'>") < 128
    work = base / 'original'
    work.mkdir()
    for p in manifest:
        if p.startswith('better_exceptions/'):
            continue
        q = work / p
        q.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(original / p, q)
    assert not (work / 'better_exceptions').exists()
    # Real supplied python/python3 commands retain the unchanged spawn-python golden.
    audit = base / 'origin-audit.jsonl'
    violation = base / 'origin-violation.jsonl'
    guard = '''import hashlib, importlib.abc, importlib.machinery, json, os, pathlib, sys
site = pathlib.Path(SITE).resolve(); alias = pathlib.Path(ALIAS); expected = EXPECTED
audit = AUDIT; violation = VIOLATION
def record(path, obj):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    try: os.write(fd, (json.dumps(obj, sort_keys=True) + "\\n").encode())
    finally: os.close(fd)
def fail(message):
    record(violation, {'pid': os.getpid(), 'failure': message}); os._exit(86)
try:
    if sys.version_info[:2] != (3, 11): fail('interpreter')
    if any(n == 'better_exceptions' or n.startswith('better_exceptions.') for n in sys.modules): fail('preloaded candidate')
    for p, h in expected.items():
        q = site / p
        if q.is_symlink() or not q.is_file() or hashlib.sha256(q.read_bytes()).hexdigest() != h: fail('runtime bytes')
    if not alias.is_symlink() or alias.resolve() != site: fail('import alias')
    sys.path.insert(0, str(alias))
    class Guard(importlib.abc.MetaPathFinder):
        def find_spec(self, fullname, path=None, target=None):
            if fullname == 'better_exceptions' or fullname.startswith('better_exceptions.'):
                try:
                    spec = importlib.machinery.PathFinder.find_spec(fullname, path)
                    if not spec or not spec.origin: fail('missing candidate')
                    q = pathlib.Path(spec.origin).resolve(); rel = q.relative_to(site).as_posix()
                    if rel not in expected or hashlib.sha256(q.read_bytes()).hexdigest() != expected[rel]: fail('shadow import')
                    record(audit, {'pid': os.getpid(), 'module': fullname, 'origin': str(q), 'sha256': expected[rel]})
                    return spec
                except BaseException: fail('origin guard')
            return None
    sys.meta_path.insert(0, Guard())
    record(audit, {'pid': os.getpid(), 'guard_ready': True, 'python': list(sys.version_info[:3]), 'site': str(site)})
except BaseException: fail('startup guard')
'''.replace('SITE', repr(str(site))).replace('ALIAS', repr(str(alias))).replace('EXPECTED', repr(runtime)).replace('AUDIT', repr(str(audit))).replace('VIOLATION', repr(str(violation)))
    (work / 'sitecustomize.py').write_text(guard)
    env = dict(os.environ)
    for key in ('PYTHONHOME', 'PYTHONSTARTUP', 'PYTHONPATH', 'COVERAGE_PROCESS_START', 'PYTEST_ADDOPTS', 'PYTEST_PLUGINS', 'BETTER_EXCEPTIONS', 'BETEXC_PYTHON', 'PYTHON', 'TERMINFO', 'TERMINFO_DIRS'):
        env.pop(key, None)
    env.update(PATH='/usr/bin:/bin', PYTHONPATH=str(work),
               PYTHONDONTWRITEBYTECODE='1', PYTHONNOUSERSITE='1', PYTHON='python3')
    # Separate preflight stdout, never mixed into unchanged golden streams.
    preflight = '''import importlib.metadata, json, pathlib, sys, curses
import better_exceptions
assert better_exceptions.__version__ == '0.4.0'
assert importlib.metadata.version('better-exceptions') == '0.4.0'
for term in ('xterm', 'vt100', 'dumb'):
    # setupterm caches per process, so a fresh subprocess checks each below.
    pass
print(json.dumps({'runtime_origin': better_exceptions.__file__, 'interpreter': str(pathlib.Path(sys.executable).resolve()), 'version': better_exceptions.__version__}))
'''
    proof = subprocess.check_output(['python3', '-c', preflight], cwd=work, env=env, text=True)
    print(proof, end='')
    for term in ('xterm', 'vt100', 'dumb'):
        subprocess.run(['python3', '-c', 'import curses; curses.setupterm(); assert curses.tigetstr("clear") is not None or __import__("os").environ["TERM"] == "dumb"'], cwd=work, env=dict(env, TERM=term), check=True)
    metadata = pathlib.Path(subprocess.check_output(['python3', '-c', 'import importlib.metadata; d=importlib.metadata.distribution("better-exceptions"); assert d.version=="0.4.0"; print(d._path)'], cwd=work, env=env, text=True).strip()).resolve()
    metadata.relative_to(site)
    for q in metadata.rglob('*'):
        if q.is_file(): owned(q)
    ready_before = {r['pid'] for r in map(json.loads, audit.read_text().splitlines()) if r.get('guard_ready')}
    assert len(ready_before) == 5
    # Exact current GHA command, no generate argument, filtering, pin or new skip.
    result = subprocess.run(['./test_all.sh'], cwd=work, env=env, capture_output=True)
    sys.stdout.buffer.write(result.stdout); sys.stderr.buffer.write(result.stderr)
    assert result.returncode == 0
    assert not violation.exists()
    stderr = re.sub(rb'\x1b\[[0-9;]*m', b'', result.stderr).decode()
    variants = [f'test/output/python3-{term}-{encoding}-{color}.out'
                for encoding in ('ascii', 'UTF-8') for term in ('xterm', 'vt100', 'dumb')
                for color in ('nocolor', 'color')]
    assert len(variants) == 12 and all(stderr.count(p) == 1 for p in variants)
    cases = ['python3 test/test.py', 'python3 test/test_color.py', 'python3 test/test_encoding.py',
             './test/test_interactive.sh', './test/test_string.sh', 'python3 test/test_logging.py',
             'python3 test/test_truncating.py', 'python3 test/test_truncating_disabled.py',
             'python3 test/test_indentation_error.py', 'python3 test/test_syntax_error.py']
    assert all(stderr.count(command) == 12 for command in cases)
    rows = [json.loads(line) for line in audit.read_text().splitlines()]
    assert any(r.get('module') == 'better_exceptions' for r in rows)
    assert all(not r.get('failure') for r in rows)
    ready_after = [r['pid'] for r in rows if r.get('guard_ready')]
    assert len(ready_after) == len(set(ready_after)) == 185
    suite_pids = set(ready_after) - ready_before
    assert len(suite_pids) == 180  # 12 variants * (8 scripts + 1 REPL + 6 -c calls)
    assert {r['pid'] for r in rows if r.get('module') == 'better_exceptions'} >= suite_pids
    # Independent startup contract: unchanged .pth is inert when opt-in is absent.
    # For wheel stage only, explicitly process the staged site just as RPM startup does.
    startup = '''import hashlib, importlib.metadata, json, os, pathlib, site, sys
root = pathlib.Path(ROOT).resolve()
site.addsitedir(str(root))
assert importlib.metadata.version('better-exceptions') == '0.4.0'
flag = 'BETTER_EXCEPTIONS' in os.environ
if flag:
    import better_exceptions
    p = pathlib.Path(better_exceptions.__file__).resolve()
    assert p == root / 'better_exceptions/__init__.py' and hashlib.sha256(p.read_bytes()).hexdigest() == INIT_HASH
    expected = RUNTIME_HASHES
    for name, module in tuple(sys.modules.items()):
        if name == 'better_exceptions' or name.startswith('better_exceptions.'):
            p = pathlib.Path(module.__file__).resolve(); rel = p.relative_to(root).as_posix()
            assert rel in expected and hashlib.sha256(p.read_bytes()).hexdigest() == expected[rel]
    assert sys.excepthook is better_exceptions.excepthook
else:
    assert 'better_exceptions' not in sys.modules and sys.excepthook is sys.__excepthook__
print(json.dumps({'startup_opt_in': flag, 'root': str(root), 'pth_sha256': PTH_HASH}))
'''.replace('ROOT', repr(str(site))).replace('INIT_HASH', repr(runtime['better_exceptions/__init__.py'])).replace('PTH_HASH', repr(runtime[pth])).replace('RUNTIME_HASHES', repr(runtime))
    startup_env = dict(env)
    startup_env.pop('PYTHONPATH', None)
    for opt_in in (False, True):
        e = dict(startup_env)
        if opt_in: e['BETTER_EXCEPTIONS'] = '1'
        subprocess.run([str(executable), '-c', startup], cwd=base, env=e, check=True)
    for p, h in manifest.items():
        if not p.startswith('better_exceptions/'):
            assert digest(work / p) == h
    pristine()
    print(json.dumps({'original_files': 47, 'runtime_files': 8, 'startup_pth_files': 1,
                     'original_command': ['./test_all.sh'], 'golden_variants': 12, 'active_case_invocations': 120,
                     'guarded_suite_python_processes': 180, 'guard_audit_records': len(rows), 'installed_RPM': installed,
                     'boundary': 'Original expected-exception normalization and twelve exact golden diffs retained. Source runtime excluded only from test scratch; every candidate import checks actual staged/installed bytes, out-of-band violations cannot be masked by original ||true. Original commented cases/interpreter matrix not claimed; no coverage, timing, native or performance claim.'}))

PY

%files
%license LICENSE.txt PYTHON-LICENSE.txt PYTEST-COV-MIT-LICENSE.txt BETTER-ATTRIBUTION.txt
%doc README.md PYTEST-COV-AUTHORS.rst
%{python3_sitelib}/better_exceptions/
%{python3_sitelib}/better_exceptions-*.dist-info/
%{python3_sitelib}/better_exceptions_hook.pth
%{_datadir}/python-better-exceptions/

%changelog
* Wed Oct 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.0-2
- Keep golden normalization intact using a short, verified import-path alias.

* Wed Oct 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.0-1
- Retain original terminal golden defaults and copied-code full attribution.
