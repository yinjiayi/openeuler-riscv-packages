#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python-click-aliases
env -u PYTHONHOME -u PYTHONSTARTUP -u COVERAGE_PROCESS_START -u PYTEST_ADDOPTS -u PYTEST_PLUGINS -u PYTHONPATH python3 - /usr/share/python-click-aliases/original /usr/lib/python3.11/site-packages installed <<'PY'
import hashlib,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text());runtime={p:h for p,h in manifest.items() if p.startswith('click_aliases/') and p in ('click_aliases/__init__.py','click_aliases/py.typed')}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%{NAME}',str(p)],text=True)=='python-click-aliases'
assert len(manifest)==21 and len(runtime)==2
for p,h in manifest.items():
    q=original/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
for p,h in runtime.items():
    q=site/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
for p in (site/'click_aliases').rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(site).as_posix()
    if rel not in runtime:assert p.parent.name=='__pycache__' and p.suffix=='.pyc' and any(p.name.startswith(pathlib.Path(x).stem+'.') and p.parent.parent==site/pathlib.Path(x).parent for x in runtime if x.endswith('.py')),rel
    owned(p)
archive=original.parent/'python-click-aliases-1.0.7.tar.gz';assert digest(archive)=='51866180740c4ead2c9b73da9347ec48932bd1e2a9104d534bda110259c87c74';owned(archive);owned(original.parent/'original-files.json')
for p in original.rglob('*'):
    if p.is_file() and p.relative_to(original).as_posix() not in manifest:assert p.parent.name=='__pycache__' and p.suffix=='.pyc' and any(p.name.startswith(pathlib.Path(x).stem+'.') and p.parent.parent==original/pathlib.Path(x).parent for x in manifest if x.endswith('.py'))
guard="""import hashlib,importlib.abc,importlib.machinery,importlib.metadata,json,os,pathlib,sys
site=pathlib.Path(SITE_JSON).resolve();expected=HASH_JSON
def fail_closed():os._exit(86)
if sys.version_info[:2]!=(3,11) or any(n=='click_aliases' or n.startswith('click_aliases.') for n in sys.modules):fail_closed()
try:
    if importlib.metadata.version('click')!='8.1.7' or importlib.metadata.version('pytest')!='7.4.4':fail_closed()
except BaseException:fail_closed()
class OriginGuard(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname=='click_aliases' or fullname.startswith('click_aliases.'):
            try:
                spec=importlib.machinery.PathFinder.find_spec(fullname,path)
                if not spec or not spec.origin:fail_closed()
                p=pathlib.Path(spec.origin).resolve();rel=p.relative_to(site).as_posix()
                if rel not in expected or hashlib.sha256(p.read_bytes()).hexdigest()!=expected[rel]:fail_closed()
                return spec
            except BaseException:fail_closed()
        return None
sys.meta_path.insert(0,OriginGuard())
try:
    import click_aliases
    p=pathlib.Path(click_aliases.__file__).resolve()
    if p!=site/'click_aliases/__init__.py':fail_closed()
    print(json.dumps({'guarded_runtime_origin':str(p),'runtime_sha256':expected,'python':list(sys.version_info[:3]),'click':importlib.metadata.version('click'),'pytest':importlib.metadata.version('pytest')}),file=sys.stderr)
except BaseException:fail_closed()
""".replace('SITE_JSON',repr(str(site))).replace('HASH_JSON',repr(runtime))
with tempfile.TemporaryDirectory(prefix='python-click-aliases-defaults-') as scratch:
    work=pathlib.Path(scratch)/'original';work.mkdir()
    for p in manifest:
        if p.startswith('click_aliases/'):continue
        dst=work/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/p,dst)
    assert not (work/'click_aliases').exists()
    env=dict(os.environ)
    for key in ('PYTHONHOME','PYTHONSTARTUP','COVERAGE_PROCESS_START','PYTEST_ADDOPTS','PYTEST_PLUGINS'):env.pop(key,None)
    env.update(PYTHONPATH=str(site),PYTHONDONTWRITEBYTECODE='1',PYTHONNOUSERSITE='1')
    code=guard+'\nd=importlib.metadata.distribution("click-aliases");assert d.version=="1.0.7";p=pathlib.Path(d._path).resolve();p.relative_to(site);print(str(p))\n'
    metadata=pathlib.Path(subprocess.check_output([sys.executable,'-c',code],cwd=work,env=env,text=True).strip())
    for p in metadata.rglob('*'):
        if p.is_file():owned(p)
    # Exact original current GHA command: python -m pytest, no additional arguments.
    code=guard+'\nimport runpy\nsys.argv=["pytest"]\nrunpy.run_module("pytest",run_name="__main__")\n'
    subprocess.run([sys.executable,'-c',code],cwd=work,env=env,check=True)
    for p,h in manifest.items():assert digest(original/p)==h
    for p,h in runtime.items():assert digest(site/p)==h
    print(json.dumps({'route':'Original GHA CPython3.11 command python -m pytest on distribution Click8.1.7/pytest7.4.4','original_files':21,'runtime_files':2,'original_commands':[['python','-m','pytest']],'runtime_origin':str(site/'click_aliases'),'engine':'installed-RPM' if installed else 'buildroot-wheel','boundary':'All9 original tests/assertions/config retained, no filter/new skip/pin relaxation. Legacy tox/Travis interpreter and Click5-7 matrices plus developer Poetry lock and lint/coverage/publish routes remain preserved but unclaimed.'}))
PY
