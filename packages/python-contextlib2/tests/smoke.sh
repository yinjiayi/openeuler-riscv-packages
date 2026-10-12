#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python-contextlib2
env -u PYTHONHOME -u PYTHONSTARTUP -u COVERAGE_PROCESS_START -u PYTEST_ADDOPTS -u PYTEST_PLUGINS -u PYTHONPATH python3 - /usr/share/python-contextlib2/original /usr/lib/python3.11/site-packages installed <<'PY'
import hashlib,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text())
runtime={p.removeprefix('contextlib2/'):h for p,h in manifest.items() if p.startswith('contextlib2/')}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%{NAME}',str(p)],text=True)=='python-contextlib2'
assert len(manifest)==30 and set(runtime)=={'__init__.py','__init__.pyi','py.typed'}
for p,h in manifest.items():
    q=original/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
for p,h in runtime.items():
    q=site/'contextlib2'/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
archive=original.parent/'python-contextlib2-21.6.0.tar.gz';license_text=original.parent/'TYPESHED-LICENSE.txt'
assert digest(archive)=='4c541b6043ab276d80b906783573a2d2d190843957858a7ae7917f94d906538b' and digest(license_text)=='b41b78f562a2e65b75cab44354335f6f435d4ef73065509600ac910cf4e22fe0'
owned(archive);owned(license_text);owned(original.parent/'original-files.json')
for base,expected in ((original,manifest),(site/'contextlib2',runtime)):
    for p in base.rglob('*'):
        if not p.is_file():continue
        rel=p.relative_to(base).as_posix()
        if rel in expected:continue
        assert p.parent.name=='__pycache__' and p.suffix=='.pyc' and any(p.name.startswith(pathlib.Path(x).stem+'.') and p.parent.parent==base/pathlib.Path(x).parent for x in expected if x.endswith('.py')),rel
        owned(p)
guard="""import hashlib,importlib.abc,importlib.machinery,importlib.metadata,json,os,pathlib,sys
site=pathlib.Path(SITE_JSON).resolve();expected=json.loads(RUNTIME_JSON)
def fail_closed():os._exit(86)
if any(n=='contextlib2' or n.startswith('contextlib2.') for n in sys.modules):fail_closed()
class OriginGuard(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname=='contextlib2' or fullname.startswith('contextlib2.'):
            try:
                spec=importlib.machinery.PathFinder.find_spec(fullname,path)
                if not spec or not spec.origin:fail_closed()
                p=pathlib.Path(spec.origin).resolve();rel=p.relative_to(site/'contextlib2').as_posix()
                if rel not in expected or hashlib.sha256(p.read_bytes()).hexdigest()!=expected[rel]:fail_closed()
                return spec
            except BaseException:fail_closed()
        return None
sys.meta_path.insert(0,OriginGuard())
# Verify guarded runtime first, then unload only candidate modules so original
# coverage discovery still measures their complete top-level code.
try:
    import contextlib2
    p=pathlib.Path(contextlib2.__file__).resolve()
    if p!=site/'contextlib2'/'__init__.py' or hashlib.sha256(p.read_bytes()).hexdigest()!=expected['__init__.py']:fail_closed()
    print(json.dumps({'guarded_runtime_origin':str(p),'sha256':expected['__init__.py']}),file=sys.stderr)
    for n in list(sys.modules):
        if n=='contextlib2' or n.startswith('contextlib2.'):del sys.modules[n]
except BaseException:fail_closed()
# The original discovery imports its unchanged scratch test/support package.
# It cannot import a source contextlib2 package because that copy is absent.
""".replace('SITE_JSON',repr(str(site))).replace('RUNTIME_JSON',repr(json.dumps(runtime)))
commands=[['coverage','run','-m','unittest','discover','-t','.','-s','test'],['coverage','report'],['coverage','xml'],['python','-m','mypy.stubtest','--allowlist','dev/mypy.allowlist','contextlib2']]
with tempfile.TemporaryDirectory(prefix='python-contextlib2-defaults-') as scratch:
    work=pathlib.Path(scratch)/'original';work.mkdir()
    for p in manifest:
        if p.startswith('contextlib2/'):continue
        dst=work/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/p,dst)
    assert not (work/'contextlib2').exists()
    env=dict(os.environ)
    for key in ('PYTHONHOME','PYTHONSTARTUP','COVERAGE_PROCESS_START','PYTEST_ADDOPTS','PYTEST_PLUGINS'):env.pop(key,None)
    env.update(PYTHONPATH=str(site),PYTHONDONTWRITEBYTECODE='1')
    code=guard+'\nd=importlib.metadata.distribution("contextlib2");assert d.version=="21.6.0";p=pathlib.Path(d._path).resolve();p.relative_to(site);print(str(p))\n'
    metadata_path=pathlib.Path(subprocess.check_output([sys.executable,'-c',code],cwd=work,env=env,text=True).strip())
    for p in metadata_path.rglob('*'):
        if p.is_file():owned(p)
    for argv in commands:
        if argv[0]=='coverage':module='coverage';child_argv=argv
        else:module='mypy.stubtest';child_argv=['mypy.stubtest',*argv[3:]]
        code=guard+'\nimport runpy\nsys.argv='+repr(child_argv)+'\nrunpy.run_module('+repr(module)+',run_name="__main__")\n'
        subprocess.run([sys.executable,'-c',code],cwd=work,env=env,check=True)
    print(json.dumps({'route':'Complete original CPython tox coverage/unittest/stubtest commands on target Python3.11','original_files':len(manifest),'runtime_files':len(runtime),'commands':commands,'distribution':'contextlib2','runtime_origin':str(site/'contextlib2'),'engine':'installed-RPM' if installed else 'buildroot-wheel','boundary':'All original unit tests, support, coverage settings and two-entry mypy allowlist retained byte-identical; no added filter, skip, xfail or waiver. Legacy interpreter matrix, CI orchestration and external Codecov/PyPI upload remain unclaimed.'}))
PY
