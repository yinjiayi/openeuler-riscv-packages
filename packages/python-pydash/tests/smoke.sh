#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python-pydash
python3 -I - /usr/share/python-pydash/original /usr/lib/python3.11/site-packages installed <<'PY'
import ast,hashlib,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile,xml.etree.ElementTree as ET
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text())
assert sys.version_info[:2]==(3,11) and len(manifest)==76
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%{NAME}',str(p)],text=True)=='python-pydash'
for rel,h in manifest.items():
    p=original/rel;assert p.is_file() and not p.is_symlink() and digest(p)==h;owned(p)
for p in original.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(original).as_posix()
    if rel in manifest:continue
    assert p.parent.name=='__pycache__' and p.suffix=='.pyc' and any(p.name.startswith(pathlib.Path(x).stem+'.') and p.parent.parent==original/pathlib.Path(x).parent for x in manifest if x.endswith('.py')),rel
    owned(p)
runtime={rel:site/rel.removeprefix('src/') for rel in manifest if rel.startswith('src/pydash/')}
assert runtime and 'src/pydash/__init__.py' in runtime and 'src/pydash/py.typed' in runtime and 'src/pydash/chaining/all_funcs.pyi' in runtime
for rel,p in runtime.items():assert p.is_file() and not p.is_symlink() and digest(p)==manifest[rel];owned(p)
archive=original.parent/'python-pydash-8.1.0.tar.gz'
assert digest(archive)=='d7b227c8c4998fbd24858ed54f4adfc62b95d080bd513eebd379cb35caca5e23';owned(archive);owned(original.parent/'original-files.json')
dist=[d for d in importlib.metadata.distributions(path=[str(site)]) if (d.metadata['Name'] or '').replace('_','-')=='pydash']
assert len(dist)==1 and dist[0].version=='8.1.0'
metadata=pathlib.Path(dist[0]._path).resolve();metadata.relative_to(site)
for p in metadata.rglob('*'):
    if p.is_file():owned(p)
modules={rel.removeprefix('src/').removesuffix('.py').replace('/','.').removesuffix('.__init__'):str(p) for rel,p in runtime.items() if rel.endswith('.py')}
module_digests={name:digest(pathlib.Path(p)) for name,p in modules.items()}
guard="""import hashlib,importlib.abc,importlib.util,os,pathlib,sys,traceback
try:
    modules=MODULE_FILES
    digests=MODULE_DIGESTS
    class InstalledPydashGuard(importlib.abc.MetaPathFinder):
        def find_spec(self,fullname,path=None,target=None):
            if not (fullname=='pydash' or fullname.startswith('pydash.')):return None
            try:
                assert fullname in modules,'Unmanifested candidate module: '+fullname
                p=pathlib.Path(modules[fullname]);kwargs={'submodule_search_locations':[str(p.parent)]} if p.name=='__init__.py' else {}
                assert p.is_absolute() and p.is_file() and not p.is_symlink() and hashlib.sha256(p.read_bytes()).hexdigest()==digests[fullname]
                spec=importlib.util.spec_from_file_location(fullname,str(p),**kwargs)
                assert spec is not None and spec.loader is not None and pathlib.Path(spec.origin).resolve()==p.resolve()
                return spec
            except BaseException:
                traceback.print_exc();os._exit(88)
    sys.meta_path.insert(0,InstalledPydashGuard())
    import pydash
    assert pathlib.Path(pydash.__file__).resolve()==pathlib.Path(modules['pydash']).resolve()
    loaded=[name for name in sys.modules if name=='pydash' or name.startswith('pydash.')]
    for name in loaded:
        assert name in modules and pathlib.Path(sys.modules[name].__file__).resolve()==pathlib.Path(modules[name]).resolve()
        assert hashlib.sha256(pathlib.Path(modules[name]).read_bytes()).hexdigest()==digests[name]
    print('PYDASH_DEFAULT_ORIGIN='+str(pydash.__file__),flush=True)
    # Preserve import finder but unload only this candidate after preflight so pytest-cov
    # measures the untouched module top-level statements on subsequent original imports.
    for name in loaded:del sys.modules[name]
except BaseException:
    traceback.print_exc();os._exit(88)
""".replace('MODULE_FILES',repr(modules)).replace('MODULE_DIGESTS',repr(module_digests))
observer="""import json,os,pathlib,sys
counts={'passed':0,'failed':0,'skipped':0,'xfail':0};nodeids=[]
def pytest_collection_finish(session):nodeids.extend(item.nodeid for item in session.items)
def pytest_runtest_logreport(report):
    if hasattr(report,'wasxfail'):counts['xfail']+=1
    if report.failed:counts['failed']+=1
    if report.skipped:counts['skipped']+=1
    if report.when=='call' and report.passed:counts['passed']+=1
def pytest_sessionfinish(session,exitstatus):
    origins={k:str(pathlib.Path(v.__file__).resolve()) for k,v in sys.modules.items() if (k=='pydash' or k.startswith('pydash.')) and getattr(v,'__file__',None)}
    pathlib.Path(os.environ['PYDASH_DEFAULT_REPORT']).write_text(json.dumps(dict(exitstatus=int(exitstatus),counts=counts,nodeids=nodeids,origins=origins)))
"""
with tempfile.TemporaryDirectory(prefix='python-pydash-defaults-') as scratch:
    root=pathlib.Path(scratch);work=root/'original';work.mkdir();hook=root/'guard';hook.mkdir()
    for rel in manifest:
        if rel.startswith('src/'):continue
        dst=work/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/rel,dst)
    assert not (work/'src').exists()
    (hook/'sitecustomize.py').write_text(guard);(hook/'pydash_default_observer.py').write_text(observer)
    env=dict(os.environ,PYTHONPATH=str(hook)+os.pathsep+str(site),PYTHONDONTWRITEBYTECODE='1',PYTHONNOUSERSITE='1',PYTEST_PLUGINS='pydash_default_observer',PYDASH_DEFAULT_REPORT=str(root/'report.json'),TOX_ENV_SITE_PACKAGES_DIR=str(site),COVERAGE_FILE=str(root/'.coverage'))
    for inherited in ('PYTEST_ADDOPTS','PYTHONHOME','PYTHONSTARTUP','COVERAGE_PROCESS_START','COVERAGE_RCFILE','PYTEST_DISABLE_PLUGIN_AUTOLOAD'):env.pop(inherited,None)
    # Run the unchanged original Invoke test task: exact default optional type-test exclusion,
    # actual upstream site-package relocation, all module doctests, original 100% coverage gate.
    subprocess.run([sys.executable,'-m','invoke','test'],cwd=work,env=env,check=True)
    report=json.loads((root/'report.json').read_text());counts=report['counts'];nodes=report['nodeids']
    assert report['exitstatus']==0 and len(nodes)==len(set(nodes))==counts['passed'] and counts['failed']==counts['skipped']==counts['xfail']==0
    expected_tests=[]
    for p in (original/'tests').glob('test_*.py'):
        expected_tests.extend((p.name,n.name) for n in ast.walk(ast.parse(p.read_text())) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name.startswith('test_'))
    assert len(expected_tests)==410 and all(any(pathlib.PurePosixPath(node.split('::')[0]).name==filename and node.split('::')[-1].split('[',1)[0]==name for node in nodes) for filename,name in expected_tests)
    assert not any('pytest_mypy_testing' in node for node in nodes) and any('pydash' in node and 'tests/test_' not in node for node in nodes)
    assert set(report['origins'])==set(modules)
    for name,p in report['origins'].items():assert pathlib.Path(p).resolve()==pathlib.Path(modules[name]).resolve()
    cov=ET.parse(work/'build/coverage/coverage.xml').getroot();assert int(cov.attrib['lines-valid'])>0 and int(cov.attrib['lines-covered'])==int(cov.attrib['lines-valid']) and float(cov.attrib['line-rate'])==1.0
    for rel,h in manifest.items():
        assert digest(original/rel)==h
        if rel not in runtime:assert digest(work/rel)==h
    for rel,p in runtime.items():assert digest(p)==manifest[rel]
    print('PYDASH_DEFAULT_RESULT='+json.dumps(dict(command=['python3','-m','invoke','test'],original_files=76,runtime_files=len(runtime),static_test_functions=410,actual_test_count=len(nodes),engine='installed-RPM' if installed else 'buildroot-wheel',coverage=cov.attrib,report=report,boundary='Unchanged original Invoke default test task, all core tests and module doctests, exact upstream optional mypy-tests exclusion and original coverage100. Separate inv ci docs/lint, optional with-mypy-tests, and full tox interpreter matrix are retained but unclaimed. License-only backend metadata patch does not alter pristine tests/config/license.')))
PY
