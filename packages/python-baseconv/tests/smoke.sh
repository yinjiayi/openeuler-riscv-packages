#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python-baseconv
python3 -I - /usr/share/python-baseconv/original /usr/lib/python3.11/site-packages installed <<'PY'
import hashlib,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile
assert sys.version_info[:2]==(3,11)
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%{NAME}',str(p)],text=True)=='python-baseconv'
assert len(manifest)==7
for p,h in manifest.items():
    q=original/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
for p in original.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(original).as_posix()
    if rel in manifest:continue
    assert p.parent.name=='__pycache__' and p.suffix=='.pyc' and any(p.name.startswith(pathlib.Path(x).stem+'.') and p.parent.parent==original/pathlib.Path(x).parent for x in manifest if x.endswith('.py')),rel
    owned(p)
runtime=site/'baseconv.py';assert runtime.is_file() and not runtime.is_symlink() and digest(runtime)=='8488a09e2ee890bef2e82703fe377669f734cd12ef03cdc9462944723fe349c5';owned(runtime)
for name,h in [('python-baseconv-1.2.2.tar.gz','76cf00bf469dfad0e62a2e9af1200aa985f0f076ac4b2b044d0ff1829feef79a'),('0001-python3-complete-defaults.patch','b80d02df4bac4b7034f56d735986d7481c503832656561cc464ff7a2cf80cbad')]:
    p=original.parent/name;assert p.is_file() and not p.is_symlink() and digest(p)==h;owned(p)
owned(original.parent/'original-files.json')
dist=[d for d in importlib.metadata.distributions(path=[str(site)]) if d.metadata['Name']=='python-baseconv']
assert len(dist)==1 and dist[0].version=='1.2.2'
metadata=pathlib.Path(dist[0]._path).resolve();metadata.relative_to(site)
for p in metadata.rglob('*'):
    if p.is_file():owned(p)
guard="""import hashlib,importlib.abc,importlib.util,os,pathlib,sys,traceback
try:
    runtime=pathlib.Path(RUNTIME_PATH).resolve()
    assert sys.version_info[:2]==(3,11)
    assert hashlib.sha256(runtime.read_bytes()).hexdigest()==EXPECTED_SHA
    class InstalledBaseconvGuard(importlib.abc.MetaPathFinder):
        def find_spec(self,fullname,path=None,target=None):
            if fullname=='baseconv':return importlib.util.spec_from_file_location(fullname,str(runtime))
            return None
    sys.meta_path.insert(0,InstalledBaseconvGuard())
    import baseconv
    assert pathlib.Path(baseconv.__file__).resolve()==runtime
    assert hashlib.sha256(pathlib.Path(baseconv.__file__).read_bytes()).hexdigest()==EXPECTED_SHA
    print('BASECONV_DEFAULT_ORIGIN='+str(runtime),flush=True)
except BaseException:
    traceback.print_exc();os._exit(88)
""".replace('RUNTIME_PATH',repr(str(runtime))).replace('EXPECTED_SHA',repr('8488a09e2ee890bef2e82703fe377669f734cd12ef03cdc9462944723fe349c5'))
with tempfile.TemporaryDirectory(prefix='python-baseconv-defaults-') as scratch:
    root=pathlib.Path(scratch);work=root/'original';work.mkdir();shim=root/'bin';shim.mkdir();hook=root/'guard';hook.mkdir()
    for p in manifest:
        if p=='baseconv.py':continue
        dst=work/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/p,dst)
    # Preserve exact default filename and all tests, executing the installed module.
    (work/'baseconv.py').symlink_to(runtime)
    assert (work/'baseconv.py').is_symlink() and os.path.samefile(work/'baseconv.py',runtime)
    assert digest(work/'baseconv.py')=='8488a09e2ee890bef2e82703fe377669f734cd12ef03cdc9462944723fe349c5'
    (shim/'coverage').write_text('#!'+str(pathlib.Path(sys.executable).resolve())+'\nfrom coverage.cmdline import main\nraise SystemExit(main())\n')
    (shim/'coverage').chmod(0o755)
    (hook/'sitecustomize.py').write_text(guard)
    env=dict(os.environ,PYTHONPATH=str(hook)+os.pathsep+str(site),PYTHONDONTWRITEBYTECODE='1',PYTHONNOUSERSITE='1',PATH=str(shim)+os.pathsep+'/usr/bin:/bin',COVERAGE_FILE=str(root/'.coverage'))
    for k in ('COVERAGE_PROCESS_START','PYTHONSTARTUP','PYTEST_ADDOPTS','PYTEST_PLUGINS'):env.pop(k,None)
    # Exact original shared Travis test argv; no original doctest/assertion removed.
    result=subprocess.run(['coverage','run','baseconv.py'],cwd=work,env=env,capture_output=True,text=True)
    sys.stdout.write(result.stdout);sys.stderr.write(result.stderr)
    assert result.returncode==0,('Original default test failure',result.returncode)
    assert 'BASECONV_DEFAULT_ORIGIN='+str(runtime) in result.stdout.splitlines()
    assert 'BASECONV_DOCTEST_RESULT attempted=20 failed=0' in result.stdout.splitlines()
    assert 'BASECONV_ROUNDTRIP_ASSERTIONS=1414' in result.stdout.splitlines()
    assert os.path.samefile(work/'baseconv.py',runtime) and digest(runtime)=='8488a09e2ee890bef2e82703fe377669f734cd12ef03cdc9462944723fe349c5'
    for p,h in manifest.items():
        assert digest(original/p)==h
        if p!='baseconv.py':assert digest(work/p)==h
    print(json.dumps({'route':'Original shared core coverage run baseconv.py on target Python3.11','original_files':7,'doctest_examples':20,'completed_assertions':1414,'command':['coverage','run','baseconv.py'],'runtime_origin':str(runtime),'engine':'installed-RPM' if installed else 'buildroot-wheel','boundary':'Complete original doctests/assertions retained with declared compatibility/failure-propagation patch. Legacy interpreter matrix and external Coveralls install/reporting remain unvalidated and uninstalled, not counted as tests passed.'}))
PY
