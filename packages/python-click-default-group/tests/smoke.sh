#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python-click-default-group
env -u PYTHONHOME -u PYTHONSTARTUP -u COVERAGE_PROCESS_START -u PYTEST_ADDOPTS -u PYTEST_PLUGINS -u PYTHONPATH python3 - /usr/share/python-click-default-group/original /usr/lib/python3.11/site-packages installed <<'PY'
import hashlib,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text());runtime_hash=manifest['click_default_group.py']
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%{NAME}',str(p)],text=True)=='python-click-default-group'
assert len(manifest)==9
for p,h in manifest.items():
    q=original/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
module=site/'click_default_group.py';assert module.is_file() and not module.is_symlink() and digest(module)==runtime_hash;owned(module)
archive=original.parent/'python-click-default-group-1.2.4.tar.gz'
assert digest(archive)=='7cc73659fa479e1a41e6a133c0233bf7162c212b34b84381a1a09e366b9c065c';owned(archive);owned(original.parent/'original-files.json')
for p in original.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(original).as_posix()
    if rel in manifest:continue
    assert p.parent.name=='__pycache__' and p.suffix=='.pyc' and any(p.name.startswith(pathlib.Path(x).stem+'.') and p.parent.parent==original/pathlib.Path(x).parent for x in manifest if x.endswith('.py')),rel
    owned(p)
guard="""import hashlib,importlib.abc,importlib.machinery,importlib.metadata,json,os,pathlib,sys
site=pathlib.Path(SITE_JSON).resolve();expected=HASH_JSON
def fail_closed():os._exit(86)
if any(n=='click_default_group' or n.startswith('click_default_group.') for n in sys.modules):fail_closed()
class OriginGuard(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname=='click_default_group' or fullname.startswith('click_default_group.'):
            try:
                spec=importlib.machinery.PathFinder.find_spec(fullname,path)
                if not spec or not spec.origin:fail_closed()
                p=pathlib.Path(spec.origin).resolve()
                if p!=site/'click_default_group.py' or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:fail_closed()
                return spec
            except BaseException:fail_closed()
        return None
sys.meta_path.insert(0,OriginGuard())
try:
    import click_default_group
    p=pathlib.Path(click_default_group.__file__).resolve()
    if p!=site/'click_default_group.py' or hashlib.sha256(p.read_bytes()).hexdigest()!=expected or click_default_group.__version__!='1.2.4':fail_closed()
    print(json.dumps({'guarded_runtime_origin':str(p),'sha256':expected}),file=sys.stderr)
except BaseException:fail_closed()
""".replace('SITE_JSON',repr(str(site))).replace('HASH_JSON',repr(runtime_hash))
commands=[['pytest']]
with tempfile.TemporaryDirectory(prefix='python-click-default-group-defaults-') as scratch:
    work=pathlib.Path(scratch)/'original';work.mkdir()
    for p in manifest:
        if p=='click_default_group.py':continue
        dst=work/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/p,dst)
    assert not (work/'click_default_group.py').exists()
    env=dict(os.environ)
    for key in ('PYTHONHOME','PYTHONSTARTUP','COVERAGE_PROCESS_START','PYTEST_ADDOPTS','PYTEST_PLUGINS'):env.pop(key,None)
    env.update(PYTHONPATH=str(site),PYTHONDONTWRITEBYTECODE='1')
    code=guard+'\nd=importlib.metadata.distribution("click-default-group");assert d.version=="1.2.4";p=pathlib.Path(d._path).resolve();p.relative_to(site);print(str(p))\n'
    metadata_path=pathlib.Path(subprocess.check_output([sys.executable,'-c',code],cwd=work,env=env,text=True).strip())
    for p in metadata_path.rglob('*'):
        if p.is_file():owned(p)
    for argv in commands:
        code=guard+'\nimport runpy\nsys.argv='+repr(argv)+'\nrunpy.run_module("pytest",run_name="__main__")\n'
        subprocess.run([sys.executable,'-c',code],cwd=work,env=env,check=True)
    print(json.dumps({'route':'Original current GitHub Actions shared bare pytest on target CPython3.11/official distro Click8.1.7','original_files':len(manifest),'commands':commands,'runtime_origin':str(module),'engine':'installed-RPM' if installed else 'buildroot-wheel','boundary':'All7 original test functions/config/assertions preserved; no filters/new skip/pin relaxation. Original Click8.1.6 and older matrix environments and legacy Travis orchestration/reporting not reproduced.'}))
PY
