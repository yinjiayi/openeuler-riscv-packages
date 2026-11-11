#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python-first
python3 -I - /usr/share/python-first/original /usr/lib/python3.11/site-packages installed <<'PY'
import hashlib,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%{NAME}',str(p)],text=True)=='python-first'
assert len(manifest)==14
for p,h in manifest.items():
    q=original/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
runtime=site/'first.py';assert runtime.is_file() and not runtime.is_symlink() and digest(runtime)==manifest['first.py'];owned(runtime)
archive=original.parent/'python-first-2.0.2.tar.gz'
assert digest(archive)=='3bef6f02707b0789003109d2bf10fe78e309510f8ccdced0f54e3a40d2787dbc';owned(archive);owned(original.parent/'original-files.json')
for p in original.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(original).as_posix()
    if rel in manifest:continue
    assert p.parent.name=='__pycache__' and p.suffix=='.pyc' and any(p.name.startswith(pathlib.Path(x).stem+'.') and p.parent.parent==original/pathlib.Path(x).parent for x in manifest if x.endswith('.py')),rel
    owned(p)
dist=[d for d in importlib.metadata.distributions(path=[str(site)]) if d.metadata['Name']=='first']
assert len(dist)==1 and dist[0].version=='2.0.2'
metadata=pathlib.Path(dist[0]._path).resolve();metadata.relative_to(site)
for p in metadata.rglob('*'):
    if p.is_file():owned(p)
guard="""import hashlib,importlib.abc,importlib.util,os,pathlib,sys,traceback
try:
    runtime=pathlib.Path(RUNTIME_PATH).resolve()
    assert sys.version_info[:2]==(3,11)
    assert hashlib.sha256(runtime.read_bytes()).hexdigest()==RUNTIME_SHA
    class InstalledFirstGuard(importlib.abc.MetaPathFinder):
        def find_spec(self,fullname,path=None,target=None):
            if fullname=='first':return importlib.util.spec_from_file_location(fullname,str(runtime))
            return None
    sys.meta_path.insert(0,InstalledFirstGuard())
    import first
    assert pathlib.Path(first.__file__).resolve()==runtime
    assert hashlib.sha256(pathlib.Path(first.__file__).read_bytes()).hexdigest()==RUNTIME_SHA
    print('FIRST_DEFAULT_ORIGIN='+str(runtime),flush=True)
except BaseException:
    traceback.print_exc();os._exit(88)
""".replace('RUNTIME_PATH',repr(str(runtime))).replace('RUNTIME_SHA',repr(manifest['first.py']))
with tempfile.TemporaryDirectory(prefix='python-first-defaults-') as scratch:
    root=pathlib.Path(scratch);work=root/'original';work.mkdir();shim=root/'bin';shim.mkdir();hook=root/'guard';hook.mkdir()
    for p in manifest:
        if p=='first.py':continue
        dst=work/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/p,dst)
    # A symlink retains pytest's first.py module-doctest discovery but executes
    # only the installed, hash-verified module. The pristine original is intact.
    (work/'first.py').symlink_to(runtime)
    assert (work/'first.py').is_symlink() and os.path.samefile(work/'first.py',runtime)
    assert digest(work/'first.py')==manifest['first.py']
    (shim/'python').symlink_to(pathlib.Path(sys.executable).resolve())
    (hook/'sitecustomize.py').write_text(guard)
    env=dict(os.environ,PYTHONPATH=str(hook)+os.pathsep+str(site),PYTHONDONTWRITEBYTECODE='1',PYTHONNOUSERSITE='1',PATH=str(shim)+os.pathsep+'/usr/bin:/bin')
    for k in ('PYTEST_ADDOPTS','PYTEST_PLUGINS'):env.pop(k,None)
    # Exact original Travis entry point and unmodified Makefile command.
    subprocess.run(['make','test'],cwd=work,env=env,check=True)
    assert os.path.samefile(work/'first.py',runtime)
    for p,h in manifest.items():assert digest(original/p)==h and digest(work/p)==h
    assert digest(runtime)==manifest['first.py']
    print(json.dumps({'route':'Original shared Travis make test on target Python3.11','original_files':14,'command':['make','test'],'original_make_argv':['python','-m','pytest','--doctest-glob=*.rst','--doctest-modules','--ignore=setup.py'],'runtime_origin':str(runtime),'engine':'installed-RPM' if installed else 'buildroot-wheel','boundary':'All original module and RST doctests/unit tests retained. Separate make cov, legacy interpreter matrix, tox manifest and external PyPI-description routes retained but unclaimed.'}))
PY
