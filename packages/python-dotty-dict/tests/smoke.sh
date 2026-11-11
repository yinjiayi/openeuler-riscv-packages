#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python-dotty-dict
python3 -I - /usr/share/python-dotty-dict/original /usr/lib/python3.11/site-packages installed <<'PY'
import hashlib,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text())
assert sys.version_info[:2]==(3,11) and len(manifest)==37
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%{NAME}',str(p)],text=True)=='python-dotty-dict'
for rel,h in manifest.items():
    p=original/rel;assert p.is_file() and not p.is_symlink() and digest(p)==h;owned(p)
for p in original.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(original).as_posix()
    if rel in manifest:continue
    assert p.parent.name=='__pycache__' and p.suffix=='.pyc' and any(p.name.startswith(pathlib.Path(x).stem+'.') and p.parent.parent==original/pathlib.Path(x).parent for x in manifest if x.endswith('.py')),rel
    owned(p)
runtime={rel:site/rel for rel in manifest if rel.startswith('dotty_dict/') and rel.endswith('.py')}
assert set(runtime)=={'dotty_dict/__init__.py','dotty_dict/dotty_dict.py'}
for rel,p in runtime.items():assert p.is_file() and not p.is_symlink() and digest(p)==manifest[rel];owned(p)
archive=original.parent/'python-dotty-dict-1.3.1.tar.gz'
assert digest(archive)=='55f6db73477790c583aba8557e6afaf8ae759253dd2ce4097ea7ae2886b1b014';owned(archive);owned(original.parent/'original-files.json')
dist=[d for d in importlib.metadata.distributions(path=[str(site)]) if (d.metadata['Name'] or '').replace('_','-')=='dotty-dict']
assert len(dist)==1 and dist[0].version=='1.3.1'
metadata=pathlib.Path(dist[0]._path).resolve();metadata.relative_to(site)
for p in metadata.rglob('*'):
    if p.is_file():owned(p)
guard="""import hashlib,importlib.abc,importlib.util,os,pathlib,sys,traceback
try:
    runtime={k:pathlib.Path(v).resolve() for k,v in RUNTIME_FILES.items()}
    class InstalledDottyGuard(importlib.abc.MetaPathFinder):
        def find_spec(self,fullname,path=None,target=None):
            if fullname=='dotty_dict':return importlib.util.spec_from_file_location(fullname,str(runtime['dotty_dict/__init__.py']),submodule_search_locations=[str(runtime['dotty_dict/__init__.py'].parent)])
            if fullname=='dotty_dict.dotty_dict':return importlib.util.spec_from_file_location(fullname,str(runtime['dotty_dict/dotty_dict.py']))
            return None
    sys.meta_path.insert(0,InstalledDottyGuard())
    import dotty_dict,dotty_dict.dotty_dict
    for name,rel in [('dotty_dict','dotty_dict/__init__.py'),('dotty_dict.dotty_dict','dotty_dict/dotty_dict.py')]:
        module=sys.modules[name];assert pathlib.Path(module.__file__).resolve()==runtime[rel]
        assert hashlib.sha256(runtime[rel].read_bytes()).hexdigest()==RUNTIME_DIGESTS[rel]
    print('DOTTY_DEFAULT_ORIGIN='+str(runtime['dotty_dict/dotty_dict.py']),flush=True)
except BaseException:
    traceback.print_exc();os._exit(88)
""".replace('RUNTIME_FILES',repr({k:str(v) for k,v in runtime.items()})).replace('RUNTIME_DIGESTS',repr({k:manifest[k] for k in runtime}))
observer="""import json,os,pathlib
counts={'passed':0,'failed':0,'skipped':0,'xfail':0};nodeids=[]
def pytest_collection_finish(session):nodeids.extend(item.nodeid for item in session.items)
def pytest_runtest_logreport(report):
    if hasattr(report,'wasxfail'):counts['xfail']+=1
    if report.failed:counts['failed']+=1
    if report.skipped:counts['skipped']+=1
    if report.when=='call' and report.passed:counts['passed']+=1
def pytest_sessionfinish(session,exitstatus):
    pathlib.Path(os.environ['DOTTY_DEFAULT_REPORT']).write_text(json.dumps(dict(exitstatus=int(exitstatus),counts=counts,nodeids=nodeids)))
"""
with tempfile.TemporaryDirectory(prefix='python-dotty-defaults-') as scratch:
    root=pathlib.Path(scratch);work=root/'original';work.mkdir();hook=root/'guard';hook.mkdir()
    for rel in manifest:
        if rel.startswith('dotty_dict/'):continue
        dst=work/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/rel,dst)
    assert not (work/'dotty_dict').exists()
    (hook/'sitecustomize.py').write_text(guard);(hook/'dotty_default_observer.py').write_text(observer)
    env=dict(os.environ,PYTHONPATH=str(hook)+os.pathsep+str(site),PYTHONDONTWRITEBYTECODE='1',PYTHONNOUSERSITE='1',PYTEST_PLUGINS='dotty_default_observer',DOTTY_DEFAULT_REPORT=str(root/'report.json'))
    env.pop('PYTEST_ADDOPTS',None)
    # Original bare pytest core suite; original pyproject addopts/testpaths unchanged.
    # Observer only records reports; it changes neither selection nor test outcomes.
    subprocess.run([sys.executable,'-m','pytest'],cwd=work,env=env,check=True)
    report=json.loads((root/'report.json').read_text());assert report['exitstatus']==0 and len(report['nodeids'])==len(set(report['nodeids']))==79 and report['counts']==dict(passed=79,failed=0,skipped=0,xfail=0)
    for rel,h in manifest.items():
        assert digest(original/rel)==h
        if rel not in runtime:assert digest(work/rel)==h
    for rel,p in runtime.items():assert digest(p)==manifest[rel]
    print('DOTTY_DEFAULT_RESULT='+json.dumps(dict(command=['python3','-m','pytest'],original_addopts='-rx -s --verbose',original_testpaths=['tests'],original_files=37,runtime_files=2,engine='installed-RPM' if installed else 'buildroot-wheel',report=report,boundary='Full original79 core tests and all example functions unchanged. TargetPython3.11 is outside old CI matrix; exactPoetrylock/devpytest7.1.2, tox/lint/docs/interpreter matrix retained but unclaimed.')))
PY
