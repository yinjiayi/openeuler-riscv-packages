#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python-better-exceptions
env -u BETTER_EXCEPTIONS -u PYTHONHOME -u PYTHONSTARTUP -u PYTHONPATH python3 - /usr/share/python-better-exceptions/original /usr/lib/python3.11/site-packages installed <<'PY'
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
        assert subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}', str(p)], text=True) == package

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
    assert subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}', str(command)], text=True).strip()
assert subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}', str(executable)], text=True).strip()
for command in ('bash', 'diff', 'sed', 'grep', 'cat', 'mkdir', 'env', 'ps'):
    tool = shutil.which(command)
    assert tool and pathlib.Path(tool).is_file()
    assert subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}', tool], text=True).strip()
assert pathlib.Path('/usr/bin/expect').is_file()
assert subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}', '/usr/bin/expect'], text=True).strip()

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
