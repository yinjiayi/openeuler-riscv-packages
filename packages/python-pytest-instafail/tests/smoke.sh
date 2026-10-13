#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python-pytest-instafail
env -u PYTHONHOME -u PYTHONSTARTUP -u COVERAGE_PROCESS_START -u PYTEST_ADDOPTS -u PYTEST_PLUGINS -u PYTEST_DISABLE_PLUGIN_AUTOLOAD -u PYTHONPATH python3 - /usr/share/python-pytest-instafail/original /usr/lib/python3.11/site-packages installed <<'PY'
import hashlib,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text())
runtime_hash='3a629075e4c0a3279c9b6ea5ac6be4777dbf5028f980353dbb80bb0da641d2e1'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%{NAME}',str(p)],text=True)=='python-pytest-instafail'
assert len(manifest)==11 and manifest['pytest_instafail.py']==runtime_hash
for p,h in manifest.items():
    q=original/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
module=site/'pytest_instafail.py';assert module.is_file() and not module.is_symlink() and digest(module)==runtime_hash;owned(module)
archive=original.parent/'python-pytest-instafail-0.5.0.tar.gz'
assert digest(archive)=='f8de1f7e72ae7fd23d46dd60863ac4b26d6d3531715c44ca4c6ed40b98d7bf5a';owned(archive);owned(original.parent/'original-files.json')
assert digest(original/'LICENSE')=='45f321ed084adee02dec233ca9704de5a88a07ca2ffe42c3784944fa6d4b0786'
for p in original.rglob('*'):
    if p.is_file():assert p.relative_to(original).as_posix() in manifest;owned(p)
guard="""import hashlib,importlib.abc,importlib.machinery,os,pathlib,sys
expected=pathlib.Path(SITE_JSON)/'pytest_instafail.py'
def fail_closed():os._exit(86)
if 'pytest_instafail' in sys.modules:fail_closed()
class OriginGuard(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname=='pytest_instafail':
            try:
                spec=importlib.machinery.PathFinder.find_spec(fullname,path)
                if not spec or not spec.origin:fail_closed()
                p=pathlib.Path(spec.origin).resolve()
                if p!=expected or hashlib.sha256(p.read_bytes()).hexdigest()!=RUNTIME_JSON:fail_closed()
                print('guarded_instafail_runtime='+str(p),file=sys.stderr)
                return spec
            except BaseException:fail_closed()
        return None
sys.meta_path.insert(0,OriginGuard())
""".replace('SITE_JSON',repr(str(site))).replace('RUNTIME_JSON',repr(runtime_hash))
with tempfile.TemporaryDirectory(prefix='python-pytest-instafail-defaults-') as scratch:
    base=pathlib.Path(scratch);work=base/'original';work.mkdir();guards=base/'guard';guards.mkdir()
    for p in manifest:
        if p=='pytest_instafail.py':continue
        dst=work/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/p,dst)
    assert not (work/'pytest_instafail.py').exists()
    (guards/'sitecustomize.py').write_text(guard)
    env=dict(os.environ)
    for key in ('PYTHONHOME','PYTHONSTARTUP','COVERAGE_PROCESS_START','PYTEST_ADDOPTS','PYTEST_PLUGINS','PYTEST_DISABLE_PLUGIN_AUTOLOAD','PYTHONPATH'):env.pop(key,None)
    env.update(PYTHONPATH=str(guards)+os.pathsep+str(site),PYTHONDONTWRITEBYTECODE='1',FORCE_COLOR='1')
    code="import importlib.metadata,pathlib;d=importlib.metadata.distribution('pytest-instafail');assert d.version=='0.5.0';p=pathlib.Path(d._path).resolve();p.relative_to(pathlib.Path("+repr(str(site))+").resolve());assert [(e.name,e.value) for e in d.entry_points if e.group=='pytest11']==[('instafail','pytest_instafail')];print(str(p))"
    meta=pathlib.Path(subprocess.check_output([sys.executable,'-c',code],cwd=work,env=env,text=True).strip())
    for p in meta.rglob('*'):
        if p.is_file():owned(p)
    # Unfiltered original tox command with no posargs; config and fixtures untouched.
    code="import runpy,sys;sys.argv=['pytest'];runpy.run_module('pytest',run_name='__main__')"
    subprocess.run([sys.executable,'-c',code],cwd=work,env=env,check=True)
    print(json.dumps({'route':'Original bare pytest command, setup.cfg --color=yes and original FORCE_COLOR=1','original_files':len(manifest),'runtime_files':1,'commands':[['pytest']],'runtime_origin':str(module),'engine':'installed-RPM' if installed else 'buildroot-wheel','boundary':'All seven original test methods and both three-way fixture parameter sets retained; no filters/new skip/xfail. Original Option sets n=None, so worker-labelled fixture cases are not claimed as xdist workers. Current Python3.11/distro pytest is tested separately from unclaimed legacy tox pytest5/6/interpreter/platform matrix.'}))
PY
