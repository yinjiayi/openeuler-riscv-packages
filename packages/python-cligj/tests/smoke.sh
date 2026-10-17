#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python-cligj
python3 - /usr/share/python-cligj/original /usr/lib/python3.11/site-packages installed <<'PY'
import hashlib,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text())
runtime={p.removeprefix('cligj/'):h for p,h in manifest.items() if p.startswith('cligj/')}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%{NAME}',str(p)],text=True)=='python-cligj'
assert len(manifest)==21 and len(runtime)==2
for p,h in manifest.items():
    q=original/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
for p,h in runtime.items():
    q=site/'cligj'/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
if installed:
    archive=original.parent/'python-cligj-0.7.2.tar.gz';assert digest(archive)=='dc340a1dcc13ba0215b7782e91bcaa45b6f36d573847ecc07ccc88c0cf8e3cd6';owned(archive);owned(original.parent/'original-files.json')
for base,expected in ((original,manifest),(site/'cligj',runtime)):
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
        if fullname=='cligj' or fullname.startswith('cligj.'):
            spec=importlib.machinery.PathFinder.find_spec(fullname,path);assert spec and spec.origin
            p=pathlib.Path(spec.origin).resolve();rel=p.relative_to(site/'cligj').as_posix()
            assert rel in expected and hashlib.sha256(p.read_bytes()).hexdigest()==expected[rel],(fullname,str(p))
            return spec
        return None
sys.meta_path.insert(0,OriginGuard())
# Do not preload runtime before original pytest-cov instrumentation.
""".replace('SITE_JSON',repr(str(site))).replace('RUNTIME_JSON',repr(json.dumps(runtime)))
with tempfile.TemporaryDirectory(prefix='python-cligj-defaults-') as scratch:
    work=pathlib.Path(scratch)/'original';work.mkdir()
    for p in manifest:
        if p.startswith('cligj/'):continue
        dst=work/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/p,dst)
    assert not (work/'cligj').exists()
    env=dict(os.environ,PYTHONPATH=str(site),PYTHONDONTWRITEBYTECODE='1')
    args=['--cov','cligj','--cov-report','term-missing']
    code=guard+'\nimport runpy\nsys.argv='+repr(['py.test']+args)+'\nrunpy.run_module("pytest",run_name="__main__")\n'
    subprocess.run([sys.executable,'-c',code],cwd=work,env=env,check=True)
    code=guard+'\nd=importlib.metadata.distribution("cligj");assert d.version=="0.7.2";p=pathlib.Path(d._path).resolve();p.relative_to(site);print(str(p))\n'
    metadata_path=pathlib.Path(subprocess.check_output([sys.executable,'-c',code],cwd=work,env=env,text=True).strip())
    for p in metadata_path.rglob('*'):
        if p.is_file():owned(p)
    print(json.dumps({'route':'Original shared Travis py.test coverage default on target Python3.11','original_files':len(manifest),'runtime_files':len(runtime),'commands':[['py.test']+args],'runtime_origin':str(site/'cligj'),'engine':'installed-RPM' if installed else 'buildroot-wheel','boundary':'Whole original tests/config/fixtures retained. Legacy interpreter matrix, external Coveralls upload and PyPI publication unclaimed.'}))
PY
