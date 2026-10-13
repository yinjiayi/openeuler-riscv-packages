#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python-pysnooper
env -u PYTHONHOME -u PYTHONSTARTUP -u COVERAGE_PROCESS_START -u PYTEST_ADDOPTS -u PYTEST_PLUGINS -u PYTHONPATH -u PYSNOOPER_DISABLED python3 - /usr/share/python-pysnooper/original /usr/lib/python3.11/site-packages installed <<'PY'
import hashlib,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text())
runtime={p.removeprefix('pysnooper/'):h for p,h in manifest.items() if p.startswith('pysnooper/')}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%{NAME}',str(p)],text=True)=='python-pysnooper'
assert len(manifest)==43 and set(runtime)=={'__init__.py','pycompat.py','tracer.py','utils.py','variables.py'}
for p,h in manifest.items():
    q=original/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
for p,h in runtime.items():
    q=site/'pysnooper'/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
archive=original.parent/'python-pysnooper-1.2.3.tar.gz';license_text=original.parent/'CONTEXTLIB2-LICENSE.txt'
assert digest(archive)=='01380deec408700ce91ebc9880991a31f0d8a171dd12a14012d7fb302df71fbc' and digest(license_text)=='c6a7affac6acdad2d2dd87d2d768438624ab692618db1f02bea3b11d3f3978f0'
owned(archive);owned(license_text);owned(original.parent/'original-files.json')
for base,expected in ((original,manifest),(site/'pysnooper',runtime)):
    for p in base.rglob('*'):
        if not p.is_file():continue
        rel=p.relative_to(base).as_posix()
        if rel in expected:continue
        assert p.parent.name=='__pycache__' and p.suffix=='.pyc' and any(p.name.startswith(pathlib.Path(x).stem+'.') and p.parent.parent==base/pathlib.Path(x).parent for x in expected if x.endswith('.py')),rel
        owned(p)
guard="""import hashlib,importlib.abc,importlib.machinery,importlib.metadata,json,os,pathlib,sys
site=pathlib.Path(SITE_JSON).resolve();expected=json.loads(RUNTIME_JSON)
def fail_closed():os._exit(86)
if any(n=='pysnooper' or n.startswith('pysnooper.') for n in sys.modules):fail_closed()
class OriginGuard(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname=='pysnooper' or fullname.startswith('pysnooper.'):
            try:
                spec=importlib.machinery.PathFinder.find_spec(fullname,path)
                if not spec or not spec.origin:fail_closed()
                p=pathlib.Path(spec.origin).resolve();rel=p.relative_to(site/'pysnooper').as_posix()
                if rel not in expected or hashlib.sha256(p.read_bytes()).hexdigest()!=expected[rel]:fail_closed()
                return spec
            except BaseException:fail_closed()
        return None
sys.meta_path.insert(0,OriginGuard())
try:
    import pysnooper
    p=pathlib.Path(pysnooper.__file__).resolve()
    if p!=site/'pysnooper'/'__init__.py' or hashlib.sha256(p.read_bytes()).hexdigest()!=expected['__init__.py']:fail_closed()
    print(json.dumps({'guarded_runtime_origin':str(p),'sha256':expected['__init__.py']}),file=sys.stderr)
except BaseException:fail_closed()
""".replace('SITE_JSON',repr(str(site))).replace('RUNTIME_JSON',repr(json.dumps(runtime)))
commands=[['pytest']]
with tempfile.TemporaryDirectory(prefix='python-pysnooper-defaults-') as scratch:
    work=pathlib.Path(scratch)/'original';work.mkdir()
    for p in manifest:
        if p.startswith('pysnooper/'):continue
        dst=work/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/p,dst)
    assert not (work/'pysnooper').exists()
    env=dict(os.environ)
    for key in ('PYTHONHOME','PYTHONSTARTUP','COVERAGE_PROCESS_START','PYTEST_ADDOPTS','PYTEST_PLUGINS','PYSNOOPER_DISABLED'):env.pop(key,None)
    env.update(PYTHONPATH=str(site),PYTHONDONTWRITEBYTECODE='1')
    code=guard+'\nd=importlib.metadata.distribution("PySnooper");assert d.version=="1.2.3";p=pathlib.Path(d._path).resolve();p.relative_to(site);print(str(p))\n'
    metadata_path=pathlib.Path(subprocess.check_output([sys.executable,'-c',code],cwd=work,env=env,text=True).strip())
    for p in metadata_path.rglob('*'):
        if p.is_file():owned(p)
    for argv in commands:
        code=guard+'\nimport runpy\nsys.argv='+repr(argv)+'\nrunpy.run_module("pytest",run_name="__main__")\n'
        subprocess.run([sys.executable,'-c',code],cwd=work,env=env,check=True)
    print(json.dumps({'route':'Original shared tox pytest {posargs} with no posargs on target Python3.11','original_files':len(manifest),'runtime_files':len(runtime),'commands':commands,'distribution':'PySnooper','runtime_origin':str(site/'pysnooper'),'engine':'installed-RPM' if installed else 'buildroot-wheel','boundary':'All original test/config/vendor/support bytes and original strict-markers/default timing tolerance retained. No filters/new skip/xfail or performance claim. Legacy interpreter/lint/security/readme/requirements/publish jobs remain unclaimed.'}))
PY
