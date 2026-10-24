#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python-makefun
env -u PYTHONHOME -u PYTHONSTARTUP -u COVERAGE_PROCESS_START -u PYTEST_ADDOPTS -u PYTEST_PLUGINS -u PYTHONPATH python3 - /usr/share/python-makefun/original /usr/lib/python3.11/site-packages installed <<'PY'
import ast,hashlib,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text());runtime={p.removeprefix('src/'):h for p,h in manifest.items() if p.startswith('src/makefun/')}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%{NAME}',str(p)],text=True)=='python-makefun'
assert len(manifest)==41 and len(runtime)==6
for p,h in manifest.items():
    q=original/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
for p,h in runtime.items():
    q=site/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
versionfile=site/'makefun/_version.py';assert versionfile.is_file() and not versionfile.is_symlink();owned(versionfile)
tree=ast.parse(versionfile.read_text());assert len(tree.body)==2
values={}
for node in tree.body:
    assert isinstance(node,ast.Assign) and len(node.targets)==2 and all(isinstance(x,ast.Name) for x in node.targets)
    for target in node.targets:values[target.id]=ast.literal_eval(node.value)
assert values=={'__version__':'1.16.0','version':'1.16.0','__version_tuple__':(1,16,0),'version_tuple':(1,16,0)}
assert tree.body[0].targets[0].id=='__version__' and tree.body[1].targets[0].id=='__version_tuple__'
runtime['makefun/_version.py']=digest(versionfile)
for p in (site/'makefun').rglob('*'):
    if not p.is_file():continue
    assert not p.is_symlink();rel=p.relative_to(site).as_posix()
    if rel not in runtime:assert p.parent.name=='__pycache__' and p.suffix=='.pyc' and any(p.name.startswith(pathlib.Path(x).stem+'.') and p.parent.parent==site/pathlib.Path(x).parent for x in runtime if x.endswith('.py')),rel
    owned(p)
archive=original.parent/'python-makefun-1.16.0.tar.gz';assert digest(archive)=='e632cd8cea81ec69ca17718896da11fb60ae472fbab186438b6703f9b176edd5';owned(archive);owned(original.parent/'original-files.json')
for name,expected in [('CC-BY-SA-4.0.txt','28a9529c7d0bb4dc51f4bf5c116a3d16ef247a052f7591466768ddf563fd1cf5'),('MAKEFUN-ATTRIBUTION.txt','1707b762021e149cc91ae26bd4d99f43b9fbf0b1102524238f881fa7fcc0f128')]:
    p=original.parent/name;assert p.is_file() and not p.is_symlink() and digest(p)==expected;owned(p)
guard="""import hashlib,importlib.abc,importlib.machinery,importlib.metadata,json,os,pathlib,sys
site=pathlib.Path(SITE_JSON).resolve();expected=HASH_JSON
def fail_closed():os._exit(86)
if sys.version_info[:2]!=(3,11) or any(n=='makefun' or n.startswith('makefun.') for n in sys.modules):fail_closed()
try:
    if importlib.metadata.version('pytest')!='7.4.4' or importlib.metadata.version('pytest-asyncio')!='0.21.1':fail_closed()
except BaseException:fail_closed()
class OriginGuard(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname=='makefun' or fullname.startswith('makefun.'):
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
    import makefun
    p=pathlib.Path(makefun.__file__).resolve()
    if p!=site/'makefun/__init__.py' or makefun.__version__!='1.16.0':fail_closed()
    print(json.dumps({'guarded_runtime_origin':str(p),'runtime_sha256':expected,'python':list(sys.version_info[:3]),'pytest':importlib.metadata.version('pytest'),'pytest_asyncio':importlib.metadata.version('pytest-asyncio')}),file=sys.stderr)
except BaseException:fail_closed()
""".replace('SITE_JSON',repr(str(site))).replace('HASH_JSON',repr(runtime))
with tempfile.TemporaryDirectory(prefix='python-makefun-defaults-') as scratch:
    work=pathlib.Path(scratch)/'original';work.mkdir()
    for p in manifest:
        if p.startswith('src/makefun/'):continue
        dst=work/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/p,dst)
    assert not (work/'src/makefun').exists()
    env=dict(os.environ)
    for key in ('PYTHONHOME','PYTHONSTARTUP','COVERAGE_PROCESS_START','PYTEST_ADDOPTS','PYTEST_PLUGINS'):env.pop(key,None)
    env.update(PYTHONPATH=str(site),PYTHONDONTWRITEBYTECODE='1',PYTHONNOUSERSITE='1')
    code=guard+'\nd=importlib.metadata.distribution("makefun");assert d.version=="1.16.0";p=pathlib.Path(d._path).resolve();p.relative_to(site);print(str(p))\n'
    metadata=pathlib.Path(subprocess.check_output([sys.executable,'-c',code],cwd=work,env=env,text=True).strip())
    for p in metadata.rglob('*'):
        if p.is_file():owned(p)
    # Original CPython3.11 nox tests session, coverage=False: unchanged argv/config.
    code=guard+'\nimport runpy\nsys.argv=["pytest","--cache-clear","-v","tests/"]\nrunpy.run_module("pytest",run_name="__main__")\n'
    subprocess.run([sys.executable,'-c',code],cwd=work,env=env,check=True)
    # Additional behavioral replay, not four extra pytest passes: unchanged bodies.
    replay=[('tests.test_generators_coroutines','test_native_coroutine'),('tests.test_generators_coroutines','test_issue_96'),('tests.test_issues','test_issue_77_async_generator_wraps'),('tests.test_issues','test_issue_77_async_generator_partial')]
    code=guard+'\nimport asyncio,importlib,inspect\nreplay='+repr(replay)+'\n'
    code+='for module,name in replay:\n m=importlib.import_module(module);p=pathlib.Path(m.__file__).resolve();rel=p.relative_to(pathlib.Path.cwd()).as_posix();assert rel in ORIGINAL_HASHES and hashlib.sha256(p.read_bytes()).hexdigest()==ORIGINAL_HASHES[rel];f=getattr(m,name);assert inspect.iscoroutinefunction(f) and len(inspect.signature(f).parameters)==0;asyncio.run(f());print(json.dumps({"supplementary_awaited_original":module+"::"+name,"source_sha256":ORIGINAL_HASHES[rel]}))\n'
    code=code.replace('ORIGINAL_HASHES',repr(manifest))
    subprocess.run([sys.executable,'-c',code],cwd=work,env=env,check=True)
    for p,h in manifest.items():assert digest(original/p)==h
    for p,h in runtime.items():assert digest(site/p)==h
    print(json.dumps({'route':'Original CPython3.11 python -m pytest --cache-clear -v tests/; supplementary four original awaited bodies','original_files':41,'runtime_files':7,'original_commands':[['python','-m','pytest','--cache-clear','-v','tests/']],'supplementary_awaited_bodies':replay,'generated_runtime_sha256':runtime['makefun/_version.py'],'engine':'installed-RPM' if installed else 'buildroot-wheel','boundary':'Original cfg doctest/ignore_glob/warnings and skips preserved. Strict-plugin four skips must be reported as skips; separate awaited assertions are not pytest passes. Other nox sessions/matrix, coverage70/report, docs/lint/build/publish unclaimed.'}))
PY
