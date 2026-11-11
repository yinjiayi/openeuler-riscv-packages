#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python-pytest-check
env -u PYTHONHOME -u PYTHONSTARTUP -u COVERAGE_PROCESS_START -u PYTEST_ADDOPTS -u PYTEST_PLUGINS -u PYTHONPATH python3 - /usr/share/python-pytest-check/original /usr/lib/python3.11/site-packages installed <<'PY'
import hashlib,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text());runtime={p.removeprefix('src/pytest_check/'):h for p,h in manifest.items() if p.startswith('src/pytest_check/')}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%{NAME}',str(p)],text=True)=='python-pytest-check'
assert len(manifest)==102 and len(runtime)==9
for p,h in manifest.items():
    q=original/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
for p,h in runtime.items():
    q=site/'pytest_check'/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
archive=original.parent/'python-pytest-check-3.0.1.tar.gz';assert digest(archive)=='6985fb29936e862873487285463049b63be9eb7feb4c8201deb224ba015cd458';owned(archive);owned(original.parent/'original-files.json')
for p in original.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(original).as_posix()
    if rel in manifest:continue
    assert p.parent.name=='__pycache__' and p.suffix=='.pyc' and any(p.name.startswith(pathlib.Path(x).stem+'.') and p.parent.parent==original/pathlib.Path(x).parent for x in manifest if x.endswith('.py')),rel
    owned(p)
guard="""import hashlib,importlib.abc,importlib.machinery,importlib.metadata,os,pathlib,sys
site=pathlib.Path(SITE_JSON).resolve();expected=RUNTIME_JSON
def fail_closed():os._exit(86)
def checked(p):
    try:
        q=pathlib.Path(p).resolve();rel=q.relative_to(site/'pytest_check').as_posix()
        if rel not in expected or hashlib.sha256(q.read_bytes()).hexdigest()!=expected[rel]:fail_closed()
    except BaseException:fail_closed()
if any(n=='pytest_check' or n.startswith('pytest_check.') for n in sys.modules):fail_closed()
for rel in expected:checked(site/'pytest_check'/rel)
class OriginGuard(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname=='pytest_check' or fullname.startswith('pytest_check.'):
            try:
                spec=importlib.machinery.PathFinder.find_spec(fullname,path)
                if not spec or not spec.origin:fail_closed()
                checked(spec.origin)
            except BaseException:fail_closed()
        # Preserve pytest's original assertion-rewriting loader rather than returning a substitute.
        return None
sys.meta_path.insert(0,OriginGuard())
def audit(event,args):
    if event=='exec':
        filename=args[0].co_filename
        if '/pytest_check/' in filename.replace(chr(92),'/'):
            checked(filename)
sys.addaudithook(audit)
try:
    d=importlib.metadata.distribution('pytest-check');p=pathlib.Path(d._path).resolve();p.relative_to(site)
    if d.version!='3.0.1':fail_closed()
    eps=[e for e in d.entry_points if e.group=='pytest11' and e.name=='check']
    if len(eps)!=1 or eps[0].value!='pytest_check.plugin':fail_closed()
except BaseException:fail_closed()
""".replace('SITE_JSON',repr(str(site))).replace('RUNTIME_JSON',repr(runtime))
with tempfile.TemporaryDirectory(prefix='python-pytest-check-defaults-') as scratch:
    work=pathlib.Path(scratch)/'original';work.mkdir();guarddir=pathlib.Path(scratch)/'guard';guarddir.mkdir();(guarddir/'sitecustomize.py').write_text(guard)
    for p in manifest:
        if p.startswith('src/pytest_check/'):continue
        dst=work/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/p,dst)
    assert not (work/'src/pytest_check').exists() and not (work/'pytest_check').exists()
    env=dict(os.environ)
    for key in ('PYTHONHOME','PYTHONSTARTUP','COVERAGE_PROCESS_START','PYTEST_ADDOPTS','PYTEST_PLUGINS'):env.pop(key,None)
    env.update(PYTHONPATH=os.pathsep.join([str(guarddir),str(site)]),PYTHONDONTWRITEBYTECODE='1')
    # Preflight executes in its own child: do not preload/unload the test child and wrap Thread.start twice.
    code="import importlib.metadata,json,pathlib,sys;d=importlib.metadata.distribution('pytest-check');e=[e for e in d.entry_points if e.group=='pytest11' and e.name=='check'][0];module=e.load();print(json.dumps({'dist':str(pathlib.Path(d._path).resolve()),'entrypoint':e.value,'runtime':str(pathlib.Path(module.__file__).resolve())}))"
    proof=json.loads(subprocess.check_output([sys.executable,'-c',code],cwd=work,env=env,text=True));assert proof['runtime']==str(site/'pytest_check/plugin.py') and proof['entrypoint']=='pytest_check.plugin'
    metadata_path=pathlib.Path(proof['dist']);metadata_path.relative_to(site)
    for p in metadata_path.rglob('*'):
        if p.is_file():owned(p)
    print(json.dumps({'preflight':proof,'runtime_hashes':runtime,'original_files':len(manifest)}),flush=True)
    # Same exact original bare pytest argv; all strict addopts/testpaths and pytester children remain original.
    code="import runpy,sys;sys.argv=['pytest'];runpy.run_module('pytest',run_name='__main__')"
    subprocess.run([sys.executable,'-c',code],cwd=work,env=env,check=True)
    print(json.dumps({'route':'Original CPython3.11 core testenv bare pytest','commands':[['pytest']],'original_files':len(manifest),'runtime_files':len(runtime),'engine':'installed-RPM' if installed else 'buildroot-wheel','boundary':'No added skips/filter/disableautoload/plugin removal. Original optional-plugin skip predicates retained. Tox orchestration and separate 3.13+/coverage100/type/lint environments unclaimed.'}))
PY
