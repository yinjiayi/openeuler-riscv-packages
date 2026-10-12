#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python-natsort
python3 - /usr/share/python-natsort/original /usr/lib/python3.11/site-packages installed <<'PY'
import hashlib,importlib.abc,importlib.machinery,json,os,pathlib,re,shutil,subprocess,sys,tempfile
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text())
runtime={p.removeprefix('natsort/'):h for p,h in manifest.items() if p.startswith('natsort/')}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%{NAME}',str(p)],text=True)=='python-natsort'
assert len(manifest)==62 and len(runtime)==12
for p,h in manifest.items():
    q=original/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
for p,h in runtime.items():
    q=site/'natsort'/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
if installed:
    archive=original.parent/'python-natsort-8.4.0.tar.gz';assert digest(archive)=='f0fdff4da8b535f475eed4b49d1942f787595558983a43a361ce9e68c3378b44';owned(archive);owned(original.parent/'original-files.json')
# Only RPM-generated Python caches of explicitly retained .py files may be extra.
for base,expected in ((original,manifest),(site/'natsort',runtime)):
    for p in base.rglob('*'):
        if not p.is_file():continue
        rel=p.relative_to(base).as_posix()
        if rel in expected:continue
        assert p.parent.name=='__pycache__' and p.suffix=='.pyc' and any(p.name.startswith(pathlib.Path(x).stem+'.') and p.parent.parent==base/pathlib.Path(x).parent for x in expected if x.endswith('.py')),rel
        owned(p)
guard="""import hashlib,importlib.abc,importlib.machinery,json,pathlib,sys
site=pathlib.Path(SITE_JSON).resolve();expected=json.loads(RUNTIME_JSON)
class OriginGuard(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname=='natsort' or fullname.startswith('natsort.'):
            spec=importlib.machinery.PathFinder.find_spec(fullname,path);assert spec and spec.origin
            p=pathlib.Path(spec.origin).resolve();rel=p.relative_to(site/'natsort').as_posix()
            assert rel in expected and hashlib.sha256(p.read_bytes()).hexdigest()==expected[rel],(fullname,str(p))
            return spec
        return None
sys.meta_path.insert(0,OriginGuard())
# Do not preload runtime before the original pytest-cov instrumentation starts.
""".replace('SITE_JSON',repr(str(site))).replace('RUNTIME_JSON',repr(json.dumps(runtime)))
with tempfile.TemporaryDirectory(prefix='python-natsort-defaults-') as scratch:
    work=pathlib.Path(scratch)/'original';work.mkdir()
    for p in manifest:
        if p.startswith('natsort/'):continue
        dst=work/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/p,dst)
    assert not (work/'natsort').exists()
    env=dict(os.environ,PYTHONPATH=str(site),PYTHONDONTWRITEBYTECODE='1');env.pop('WITH_EXTRAS',None)
    selected=[('doctest',['-o','IGNORE_EXCEPTION_DETAIL','docs/howitworks.rst']),('pytest',['README.rst','docs/examples.rst']),('pytest',['--doctest-modules',str(site/'natsort')]),('pytest',['--hypothesis-profile=slow-tests','--tb=short','--cov',str(site/'natsort'),'--cov-report','term-missing']),('coverage',['xml'])]
    for module,args in selected:
        code=guard+'\nimport runpy\nsys.argv='+repr([module]+args)+'\nrunpy.run_module('+repr(module)+',run_name="__main__")\n'
        subprocess.run([sys.executable,'-c',code],cwd=work,env=env,check=True)
    print(json.dumps({'route':'original GitHub Python3.11 -> tox py311, no extras','original_files':len(manifest),'runtime_files':len(runtime),'commands':selected,'runtime_origin':str(site/'natsort'),'engine':'installed-RPM' if installed else 'buildroot-wheel','boundary':'Original skips/configs preserved; no claim about other interpreter/extras/static jobs or performance.'}))
PY
