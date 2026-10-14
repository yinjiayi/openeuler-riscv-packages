#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python-lazy
[[ $(pwd -P) == /workspace ]]
[[ -f artifacts/repository/resolution.json ]]
if [[ -d artifacts/smoke ]]; then test_evidence_dir=artifacts/smoke; elif [[ -d artifacts/golden/python-lazy ]]; then test_evidence_dir=artifacts/golden/python-lazy; else exit 2; fi
[[ ! -e $test_evidence_dir/lazy-test-prerequisites.json ]]
printf 'd62f6ec90fa3a5c5112ad4cd364d7a75ef69778c2a432825add4164a1bd64eca  ci/run-dnf-transaction\n' | sha256sum --check --strict
# Upstream mypy extra has no minimum/version pin. Install from the sole protected
# official repository with the existing bounded transaction; not a consumer dependency.
python3 ci/run-dnf-transaction --evidence "$test_evidence_dir/lazy-test-prerequisites.json" --budget-seconds 300 --attempt-timeouts-seconds 290 --retry-delay-seconds 0 --kill-after-seconds 10 -- dnf -y --setopt=install_weak_deps=False --disablerepo='*' --enablerepo=openeuler-rva23 install -- python3-mypy
env -u PYTHONHOME -u PYTHONSTARTUP -u PYTHONPATH -u PYTEST_ADDOPTS -u PYTEST_PLUGINS -u COVERAGE_PROCESS_START python3 - /usr/share/python-lazy/original /usr/lib/python3.11/site-packages installed <<'PY'
# SPDX-License-Identifier: Apache-2.0
"""Target-only unchanged Lazy commands with exact original and runtime guards."""
import ast, hashlib, importlib, importlib.abc, importlib.util, importlib.metadata
import json, os, pathlib, runpy, shutil, subprocess, sys, tempfile, unittest

original=pathlib.Path(sys.argv[1]).resolve()
site=pathlib.Path(sys.argv[2]).resolve()
mode=sys.argv[3]
assert mode in ('source','wheel','buildroot','installed') and sys.version_info[:2]==(3,11)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((original.parent/'original-files.json').read_bytes())
assert len(manifest)==24
for name,h in manifest.items():
    p=original/name
    assert p.is_file() and not p.is_symlink() and sha(p)==h
    if mode=='installed':
        assert subprocess.check_output(['rpm','-qf','--qf','%{NAME}','--',str(p)],text=True).strip()=='python-lazy'
for filename,expected in [('lazy-2.0.tar.gz','f92ec0d32dd6bd115ddec4e3323473ebc0b682ad58c6aca78ebfd9e6d1aa5777'),('lazy-git-2.0.tar.gz','9861ab943c0720c1fa72262223c26f4002292b4ba98a4c77b200987b97594ca9')]:
    p=original.parent/filename
    assert p.is_file() and not p.is_symlink() and sha(p)==expected
    if mode=='installed':
        assert subprocess.check_output(['rpm','-qf','--qf','%{NAME}','--',str(p)],text=True).strip()=='python-lazy'
if mode=='installed':
    assert subprocess.check_output(['rpm','-qf','--qf','%{NAME}','--',str(original.parent/'original-files.json')],text=True).strip()=='python-lazy'
    licensepath=pathlib.Path('/usr/share/licenses/python-lazy/LICENSE')
    assert sha(licensepath)==manifest['LICENSE'] and subprocess.check_output(['rpm','-qf','--qf','%{NAME}','--',str(licensepath)],text=True).strip()=='python-lazy'
for key in ('PYTHONHOME','PYTHONSTARTUP','PYTHONPATH','PYTEST_ADDOPTS','PYTEST_PLUGINS','COVERAGE_PROCESS_START'):
    os.environ.pop(key,None)
os.environ['PYTHONDONTWRITEBYTECODE']='1'
runtime={n:manifest[n] for n in ('lazy/__init__.py','lazy/lazy.py','lazy/lazy.pyi','lazy/py.typed')}
for n,h in runtime.items():
    p=site/n
    assert p.is_file() and not p.is_symlink() and sha(p)==h
    if mode=='installed':
        assert subprocess.check_output(['rpm','-qf','--qf','%{NAME}','--',str(p)],text=True).strip()=='python-lazy'
if mode!='source':
    dist=[d for d in importlib.metadata.distributions(path=[str(site)]) if d.metadata['Name'].lower()=='lazy']
    assert len(dist)==1 and dist[0].version=='2.0'
assert subprocess.check_output(['rpm','-qf','--qf','%{NAME}','--',str(pathlib.Path(sys.executable).resolve())],text=True).strip()=='python3'
mypy_entry=importlib.util.find_spec('mypy.__main__')
assert mypy_entry and mypy_entry.origin
assert subprocess.check_output(['rpm','-qf','--qf','%{NAME}','--',str(pathlib.Path(mypy_entry.origin).resolve())],text=True).strip()=='python3-mypy'
mypy_version=importlib.metadata.version('mypy')
mypy_rpm=subprocess.check_output(['rpm','-q','--qf','%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}','--','python3-mypy'],text=True).strip()
testtree=ast.parse((original/'lazy/tests/test_lazy.py').read_bytes())
methods={c.name+'.'+n.name for c in testtree.body if isinstance(c,ast.ClassDef) for n in c.body if isinstance(n,ast.FunctionDef) and n.name.startswith('test')}
assert len(methods)==45 and all(not n.decorator_list for c in testtree.body if isinstance(c,ast.ClassDef) for n in c.body if isinstance(n,ast.FunctionDef) and n.name.startswith('test'))
guarded={}
def stop(reason):
    print('LAZY_ORIGIN_VIOLATION '+str(reason),file=sys.stderr,flush=True)
    os._exit(86)
with tempfile.TemporaryDirectory(prefix='lazy-default-') as scratch:
    work=pathlib.Path(scratch)
    shutil.copytree(original/'lazy',work/'lazy')
    # Type checking reads the exact wheel/RPM-derived runtime bytes, not the
    # pristine Git runtime. Tests/examples remain pristine originals.
    for n,h in runtime.items():
        shutil.copy2(site/n,work/n)
        assert sha(work/n)==h and sha(site/n)==h
    for n in ('tox.ini','pyproject.toml','setup.cfg'):
        shutil.copy2(original/n,work/n)
        assert sha(work/n)==manifest[n]
    allowed={'lazy':site/'lazy/__init__.py','lazy.lazy':site/'lazy/lazy.py',
             'lazy.tests':work/'lazy/tests/__init__.py','lazy.tests.test_lazy':work/'lazy/tests/test_lazy.py',
             'lazy.examples':work/'lazy/examples/__init__.py','lazy.examples.example':work/'lazy/examples/example.py'}
    class Loader(importlib.abc.Loader):
        def __init__(self,underlying,name):self.underlying,self.name=underlying,name
        def create_module(self,spec):return self.underlying.create_module(spec) if hasattr(self.underlying,'create_module') else None
        def exec_module(self,module):
            p=allowed[self.name].resolve()
            rel='lazy/'+str(p.relative_to(site/'lazy')) if self.name in ('lazy','lazy.lazy') else str(p.relative_to(work))
            if sha(p)!=manifest[rel]:stop('loader hash '+self.name)
            self.underlying.exec_module(module)
            if pathlib.Path(module.__file__).resolve()!=p or sha(p)!=manifest[rel]:stop('loader origin '+self.name)
            guarded[self.name]=str(p)
    class Finder(importlib.abc.MetaPathFinder):
        def find_spec(self,fullname,path=None,target=None):
            if fullname=='lazy' or fullname.startswith('lazy.'):
                try:
                    if fullname not in allowed:stop('unmanifested '+fullname)
                    p=allowed[fullname].resolve()
                    rel='lazy/'+str(p.relative_to(site/'lazy')) if fullname in ('lazy','lazy.lazy') else str(p.relative_to(work))
                    if sha(p)!=manifest[rel]:stop('spec hash '+fullname)
                    spec=importlib.util.spec_from_file_location(fullname,p,submodule_search_locations=[str(p.parent)] if p.name=='__init__.py' else None)
                    if spec is None or spec.loader is None:stop('missing spec '+fullname)
                    spec.loader=Loader(spec.loader,fullname)
                    return spec
                except BaseException as exc:stop('finder '+repr(exc))
    def audit(event,args):
        if event=='exec':
            filename=getattr(args[0],'co_filename','')
            if filename and not filename.startswith('<'):
                p=pathlib.Path(filename).resolve()
                if mode!='source' and p.is_relative_to(original/'lazy'):stop('source runtime/test exec '+filename)
                if p.is_relative_to(work/'lazy'):
                    rel=str(p.relative_to(work))
                    if rel not in manifest or sha(p)!=manifest[rel]:stop('bad test/example '+filename)
                    if rel in runtime:stop('scratch runtime exec '+filename)
                if p.is_relative_to(site/'lazy'):
                    rel='lazy/'+str(p.relative_to(site/'lazy'))
                    if rel not in runtime or sha(p)!=runtime[rel]:stop('bad runtime '+filename)
    sys.meta_path.insert(0,Finder());sys.addaudithook(audit)
    sys.path[:]=[str(work),str(site)]+[p for p in sys.path if p and not pathlib.Path(p).resolve().is_relative_to(original)]
    os.environ['PYTHONPATH']=str(site)
    importlib.import_module('lazy.lazy')
    assert guarded.get('lazy') and guarded.get('lazy.lazy')
    seen=[];results=[]
    real_start=unittest.TestResult.startTest
    def start_test(self,test):seen.append(test.id());return real_start(self,test)
    unittest.TestResult.startTest=start_test
    real_run=unittest.TextTestRunner.run
    def run_suite(self,suite):r=real_run(self,suite);results.append(r);return r
    unittest.TextTestRunner.run=run_suite
    os.chdir(work)
    commands=[['python','-m','unittest','discover'],['python','-m','mypy','--strict','--exclude','lazy/tests','lazy'],['python','lazy/examples/example.py']]
    mypy_child_code="# SPDX-License-Identifier: Apache-2.0\nimport hashlib,importlib.metadata,importlib.util,json,pathlib,runpy,subprocess,sys\nwork=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve()\nexpected=json.loads(sys.argv[3]);runtime=json.loads(sys.argv[4])\nassert pathlib.Path.cwd().resolve()==work and sys.version_info[:2]==(3,11)\nfor n,h in runtime.items():\n    p=work/n;q=site/n\n    assert p.is_file() and q.is_file() and not p.is_symlink() and not q.is_symlink()\n    assert hashlib.sha256(p.read_bytes()).hexdigest()==hashlib.sha256(q.read_bytes()).hexdigest()==h\nentry=importlib.util.find_spec('mypy.__main__');assert entry and entry.origin\np=pathlib.Path(entry.origin).resolve();assert str(p)==expected['origin'] and hashlib.sha256(p.read_bytes()).hexdigest()==expected['sha256']\nassert subprocess.check_output(['rpm','-qf','--qf','%{NAME}','--',str(p)],text=True).strip()=='python3-mypy'\nassert importlib.metadata.version('mypy')==expected['version']\nassert subprocess.check_output(['rpm','-q','--qf','%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}','--','python3-mypy'],text=True).strip()==expected['rpm']\nargv=['mypy','--strict','--exclude','lazy/tests','lazy']\nprint('LAZY_MYPY_CHILD_PROVENANCE '+json.dumps(dict(status='invocation-started-not-success',argv=argv,tool=expected,runtime_files=runtime),sort_keys=True),flush=True)\nsys.argv=argv\nrunpy.run_module('mypy',run_name='__main__',alter_sys=False)\n"
    mypy_tool=dict(origin=str(pathlib.Path(mypy_entry.origin).resolve()),sha256=sha(pathlib.Path(mypy_entry.origin).resolve()),version=mypy_version,rpm=mypy_rpm)
    child_proof=None
    for argv in commands:
        if argv==['python','-m','mypy','--strict','--exclude','lazy/tests','lazy']:
            # Mypy's normal fast_exit is os._exit; isolate it without changing
            # original argv/options or disabling fast_exit in upstream code.
            completed=subprocess.run([sys.executable,'-c',mypy_child_code,str(work),str(site),json.dumps(mypy_tool,sort_keys=True),json.dumps(runtime,sort_keys=True)],cwd=work,env=dict(os.environ),capture_output=True,text=True)
            print(completed.stdout,end='',flush=True);print(completed.stderr,end='',file=sys.stderr,flush=True)
            if completed.returncode!=0:stop('mypy child exit '+str(completed.returncode))
            proofs=[json.loads(line.removeprefix('LAZY_MYPY_CHILD_PROVENANCE ')) for line in completed.stdout.splitlines() if line.startswith('LAZY_MYPY_CHILD_PROVENANCE ')]
            assert len(proofs)==1 and proofs[0]==dict(status='invocation-started-not-success',argv=['mypy','--strict','--exclude','lazy/tests','lazy'],tool=mypy_tool,runtime_files=runtime)
            child_proof=dict(provenance=proofs[0],observed_exit=completed.returncode)
            assert sha(pathlib.Path(mypy_entry.origin).resolve())==mypy_tool['sha256']
            continue
        sys.argv=([argv[2]]+argv[3:]) if argv[1]=='-m' else argv[1:]
        try:
            if argv[1]=='-m':runpy.run_module(argv[2],run_name='__main__',alter_sys=False)
            else:runpy.run_path(argv[1],run_name='__main__')
        except SystemExit as exc:
            if exc.code not in (None,0):stop('default command exit '+repr(exc.code))
    assert child_proof is not None and child_proof['observed_exit']==0
    assert len(results)==1 and results[0].testsRun==45 and results[0].wasSuccessful()
    assert not results[0].skipped and not results[0].expectedFailures and not results[0].unexpectedSuccesses
    assert len(seen)==45 and {'.'.join(n.split('.')[-2:]) for n in seen}==methods
    for n,h in runtime.items():assert sha(site/n)==sha(work/n)==h
    for n in ('lazy/tests/__init__.py','lazy/tests/test_lazy.py','lazy/examples/__init__.py','lazy/examples/example.py','tox.ini','pyproject.toml','setup.cfg'):assert sha(work/n)==manifest[n]
    print('LAZY_DEFAULT_REPORT '+json.dumps(dict(mode=mode,commands=commands,invocation='Original argv via stdlib runpy; mypy isolated child preserves normal hard exit; not a bare launcher or interpreter-matrix claim',testsRun=45,test_ids=seen,skips=0,failures=0,errors=0,strict_mypy_exit=0,mypy_version=mypy_version,mypy_rpm=mypy_rpm,mypy_origin=mypy_entry.origin,mypy_child=child_proof,example_exit=0,origins=guarded,runtime_files=runtime,original_files=24,docs_environment='opt-in/unclaimed'),sort_keys=True))
PY
