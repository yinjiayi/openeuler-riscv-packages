#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python-pydispatcher
python3 - /usr/share/python-pydispatcher/original /usr/lib/python3.11/site-packages installed <<'PY'
import hashlib,importlib.abc,importlib.machinery,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text())
runtime={p.removeprefix('pydispatch/'):h for p,h in manifest.items() if p.startswith('pydispatch/')}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%{NAME}',str(p)],text=True)=='python-pydispatcher'
assert len(manifest)==45 and len(runtime)==6
for p,h in manifest.items():
    q=original/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
for p,h in runtime.items():
    q=site/'pydispatch'/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
if installed:
    archive=original.parent/'python-pydispatcher-2.0.7.tar.gz';assert digest(archive)=='25b3b2b036fc21246c1bad5ba289b29831ed1f128c8fd036faa9cb3f8e7dd565';owned(archive);owned(original.parent/'original-files.json')
for base,expected in ((original,manifest),(site/'pydispatch',runtime)):
    for p in base.rglob('*'):
        if not p.is_file():continue
        rel=p.relative_to(base).as_posix()
        if rel in expected:continue
        assert p.parent.name=='__pycache__' and p.suffix=='.pyc' and any(p.name.startswith(pathlib.Path(x).stem+'.') and p.parent.parent==base/pathlib.Path(x).parent for x in expected if x.endswith('.py')),rel
        owned(p)
guard="""import hashlib,importlib.abc,importlib.machinery,importlib.metadata,json,pathlib,sys
site=pathlib.Path(SITE_JSON).resolve();expected=json.loads(RUNTIME_JSON)
class OriginGuard(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname=='pydispatch' or fullname.startswith('pydispatch.'):
            spec=importlib.machinery.PathFinder.find_spec(fullname,path);assert spec and spec.origin
            p=pathlib.Path(spec.origin).resolve();rel=p.relative_to(site/'pydispatch').as_posix()
            assert rel in expected and hashlib.sha256(p.read_bytes()).hexdigest()==expected[rel],(fullname,str(p))
            return spec
        return None
sys.meta_path.insert(0,OriginGuard())
# No runtime preloading before original pytest-cov instrumentation.
""".replace('SITE_JSON',repr(str(site))).replace('RUNTIME_JSON',repr(json.dumps(runtime)))
with tempfile.TemporaryDirectory(prefix='python-pydispatcher-defaults-') as scratch:
    work=pathlib.Path(scratch)/'original';work.mkdir()
    for p in manifest:
        if p.startswith('pydispatch/'):continue
        dst=work/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/p,dst)
    assert not (work/'pydispatch').exists()
    env=dict(os.environ,PYTHONPATH=str(site),PYTHONDONTWRITEBYTECODE='1')
    args=['--cov=pydispatch','--no-cov-on-fail','--cov-report=term-missing','tests']
    code=guard+'\nimport runpy\nsys.argv='+repr(['pytest']+args)+'\nrunpy.run_module("pytest",run_name="__main__")\n'
    subprocess.run([sys.executable,'-c',code],cwd=work,env=env,check=True)
    # Original packaging test exercises importlib.metadata; verify ownership too.
    code=guard+'\nd=importlib.metadata.distribution("PyDispatcher");assert d.version=="2.0.7";p=pathlib.Path(d._path).resolve();p.relative_to(site);print(str(p))\n'
    metadata_path=pathlib.Path(subprocess.check_output([sys.executable,'-c',code],cwd=work,env=env,text=True).strip())
    for p in metadata_path.rglob('*'):
        if p.is_file():owned(p)
    print(json.dumps({'route':'Original shared tox pytest coverage default on target Python3.11','original_files':len(manifest),'runtime_files':len(runtime),'commands':[['pytest']+args],'runtime_origin':str(site/'pydispatch'),'engine':'installed-RPM' if installed else 'buildroot-wheel','boundary':'Whole tests/defaults retained; no claim about original legacy interpreter matrix, standalone nose coverage utility or native hardware.'}))
PY
