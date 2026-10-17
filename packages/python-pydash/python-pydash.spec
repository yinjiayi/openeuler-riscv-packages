# SPDX-License-Identifier: Apache-2.0
Name:           python-pydash
Version:        8.1.0
Release:        1%{?dist}
Summary:        Functional Python utility library
License:        MIT
URL:            https://github.com/dgilland/pydash
Source0:        python-pydash-8.1.0.tar.gz
Patch0:         0001-license-file-metadata.patch
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools >= 61.0
BuildRequires:  python3-wheel
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-cov
BuildRequires:  python3-typing-extensions > 3.10
BuildRequires:  python3-invoke
Requires:       python3 >= 3.10
Requires:       python3-typing-extensions > 3.10
Conflicts:      python3-typing-extensions = 4.6.0
Requires:       python3-pytest
Requires:       python3-pytest-cov
Requires:       python3-invoke

%description
Pydash supplies functional collection, array, object, string and chaining
utilities. The package also retains the complete original source and
default tests for installed-RPM origin and integrity verification.

%prep
%setup -q -n pydash-f46de3669742c075e5379c1e193c86c1c2c70dc2
mkdir -p ../pydash-pristine
cp -a . ../pydash-pristine/
%patch0 -p1

%build
SOURCE_DATE_EPOCH=315532800 %{__python3} -m pip wheel --no-deps --no-index --no-build-isolation --wheel-dir wheelhouse .

%install
%{__python3} -m pip install --no-deps --no-index --no-compile --root %{buildroot} --prefix %{_prefix} wheelhouse/pydash-8.1.0-*.whl
install -d %{buildroot}%{_datadir}/python-pydash/original
cp -a ../pydash-pristine/. %{buildroot}%{_datadir}/python-pydash/original/
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/python-pydash/python-pydash-8.1.0.tar.gz
cat > %{buildroot}%{_datadir}/python-pydash/original-files.json <<'JSON'
{".github/workflows/main.yml":"5e6069f99624f06d70d86af5ec802d1457391c729b6dce863a2fb3228f6f7eb9",".gitignore":"cbe227262d23001c1b0f9c0b276c0018eaa232083840b4ddc342521813d05fb8",".readthedocs.yaml":"8b2f502a7a3a02133c0c26aae5b15ba8e72b54e5d31d95394992c3f70ed9ba38","AUTHORS.rst":"500d24575a59f94212161326c44a3df44786f12c6f6b30f13477624448f1e2a8","CHANGELOG.rst":"260faa9c49cad4b7a5c341ee79fabd57244fe98c0b5dfe80c6a4e4e729d086f7","CONTRIBUTING.rst":"ed412e09da3066bafcc3e0b1a3014d02b638431dd352dae25a9462dd147e2d07","DEVGUIDE.rst":"cc782cdb6ee11791cfd6312b5681fb4ef42170fd7d43541e91083f57ac57dc21","LICENSE.rst":"1bba57c33cce44a00d2edf0794e14bd0c6dc1569a4e78d834c8f4103b8e9623f","MANIFEST.in":"f71f607a55cbfbfd265eec5f72fe4501a736e642f9fbffbe5b6f3b576c3b964e","README.rst":"5a3f6aa696ddac7aba3a7c9fa56b71ceee9b55d27e3189dd5df40b1d43570c16","docs/Makefile":"ad438f2abda8c9a084d9c367a1e11d428b3de493d1e11f9df1aafe4ed0aafd57","docs/_templates/.gitignore":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","docs/api.rst":"ea6cf83e76c9447336bc66031d662efb7098e89dee2fa0fce46139f5c6252e7b","docs/authors.rst":"0ba8e9a403475ae12773cfce9fc7a32bce591e9801a1adde71927982f51d901b","docs/callbacks.rst":"c3d5aa236ffa93bdc82ff4b8cc4726e4d810692c8f447e0cb1f02f817a8f00cf","docs/chaining.rst":"f5d09622236c59921ede364234e2d7677747cf669d1eebd387b4148d9d3cae13","docs/changelog.rst":"bd8b3e8b5551105b987eb3f26cc72889cf471457ed78d12d93870ab39e1ec311","docs/conf.py":"81e6286b41c389ba3ee2f20cece4894abdb25af16c22f5b0a85b0429c5a2f1a2","docs/contributing.rst":"87d5c7434971ff248a817426c2a84940b3c3ed51251ddcaed6bb8a7d85afad80","docs/deeppath.rst":"6cbb572165b472a508adf08facc5af270177db6989a1223ae7a55826f1d97b93","docs/devguide.rst":"9c08d89a25a29f5443b97db77393a7b675d8b6b33f21c67bbd439bc1b0b1c35a","docs/differences.rst":"0cab0deaa5828bb8a602694b26cbbbd1a1a0c7816f26563064169c832a4dbde3","docs/index.rst":"b405cbcec1e7f09b4f00a3199421d136005c2ca1a519cfa1f6d22922208de1fb","docs/installation.rst":"66c398a3d2ade14265dabf8347ac9c802a03fd8b31153462f1f9f1086d232cd1","docs/kudos.rst":"70c8908995dde66ed95cdcf04abec1a6f203fdb03ddc79df48b0dd38c0425920","docs/license.rst":"7194660ac4f461fe947f725bc7910c16d901cf57d748925f36b7cc45607362bc","docs/quickstart.rst":"89de5297c53260d6e82c453795b6886aed76be6feb77d4912da08996f98fb6ae","docs/templating.rst":"a33d33ad2deb689f6bb95b57f2c28d64c36d4f3cdc97a057655a463faa56e6f6","docs/upgrading.rst":"ba241716c3e7065508ff9f957507047772b9f2d63055d569e9a2a0b1a4d9f244","docs/versioning.rst":"12148d0c19e3f13259e2c27d86a724e2b80ca63851f34e7e30463c32cce8a9f7","pyproject.toml":"4b5febbdee40e30bd5d7514e6dd3ac867a69c04b0a8e50c1f69747d84ef26bd7","requirements.txt":"9d6d2c2e18451cd8eb86a739cbcb1664e4342ef4ae478266a3c333dd4f73674a","scripts/chaining_type_generator.py":"1dbdcee54e3a764dee297e2e9755553a315683d8869bdbed641bf394f3a704c7","scripts/mypy_doctests_generator.py":"9c00b897c6e267f3cf7552509e02c11892abd0aefda722c11d0bdd93ad7ff67a","src/pydash/__init__.py":"4ae71a4fbb6962cc727e34fb789fe2b81dafdbb5b4fa13a68c44ec2f68e6093a","src/pydash/arrays.py":"5a0fd4373391d4977299bbfab81e848916c4c3ab56232731e9cba9c7ff4ff57f","src/pydash/chaining/__init__.py":"3978f776e3ea8c12ea69ac8782f36ef61581d465c1bc9999ef084a389daa5f95","src/pydash/chaining/all_funcs.py":"f23488f8bf8426413417bafa25466301d1d8c37475b014f7fed19974826b8e73","src/pydash/chaining/all_funcs.pyi":"394b1298d424f13390f3c9d597055d4dd5195842a4d2e7c86e344c69393b1fde","src/pydash/chaining/chaining.py":"9a71cc08ee719c2d93e575a2a7acc9dff85c57b4a5e37fae5617b0d306b0ee16","src/pydash/collections.py":"cfb1c23c3a0ad8c738e0e4cf7b3111e853b06ed219b6b7aefb300e3717be5ace","src/pydash/exceptions.py":"133f30bb7fbdc1eec48ffc6fd476c6060b90339a766664bdc12ec54a79afab8c","src/pydash/functions.py":"fae3c2e4513042b1454f5a5f0d3bdb6b82c271fcd45806c470159b0216ba01d4","src/pydash/helpers.py":"df241626bb4bfd40fd26ca5be7ca90340aa4ecadd06cb95f9285bdeb78955bfa","src/pydash/numerical.py":"4c52e02e06d8e675e9efe12a00a39b8651489adb7834695d591790c981197720","src/pydash/objects.py":"43a2988e689e5f713cd5a389d1c33c0351ee4b679a95195ae2e7f07cbd0dcd57","src/pydash/predicates.py":"e228c7945c6afe7b8a804015e5476092293c7f0f9383d54090ca29e7cecbf8f0","src/pydash/py.typed":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","src/pydash/strings.py":"2e7c284dbdebe78fef54cc413d72817e68d06bb66667c4be7796cbefcdd3504b","src/pydash/types.py":"ca64b1b6177869e7be1a255106e15fca527a9d3bfe0cfc0eca8abd9e4aff19d8","src/pydash/utilities.py":"854deb46f5d87129d0725427564fb09c1bef9cb5f17f69519450b0557d286fa5","tasks.py":"cc9ca140bd694ef42961661773257d2d6e543bb24d540736ac8b8fb352879c89","tests/__init__.py":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","tests/conftest.py":"742d0d5951e069ec0efce6c54e0abe63d42274face5407740fdbb79a046d76c8","tests/helpers.py":"f08c49163157308df2ef9c46dd3ec7f3622a9d19220ee7c5f087c837862a9678","tests/pytest_mypy_testing/__init__.py":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","tests/pytest_mypy_testing/test_arrays.py":"1db87a58c7c9533a101ea84aee648cbaa73b264fe5737faf82411e19f7f9008b","tests/pytest_mypy_testing/test_chaining.py":"a082fa63433120fd9c34bc0f5e3df3dc10b1df366efa003f8e1746dc8be8b589","tests/pytest_mypy_testing/test_collections.py":"b08a59cfa3e3521dcd07293381bad381f4645eb62591f91481298962c82494f5","tests/pytest_mypy_testing/test_functions.py":"4842b0dd36f2f419a7a3d272f1ca1d4fd400dc954b18edb8bd7363849da705b7","tests/pytest_mypy_testing/test_numerical.py":"9e6935bd9f10a9dff62f610bbc6d88614523302ba29f9c9c9bed51e7222aad63","tests/pytest_mypy_testing/test_objects.py":"43d09e364c6e41848788e9bb5fa886d614fae926805f12f0c3f703125c2032cc","tests/pytest_mypy_testing/test_predicates.py":"200ae2ec53c1ab7ff326593674ee2695c8ba509fd930f8309830267f00fb6366","tests/pytest_mypy_testing/test_strings.py":"ca7ff3745d6e6e1ec1b6591d4fea414860d5d54a8cc090404adf0c56db53458d","tests/pytest_mypy_testing/test_utilities.py":"8a47e68c8ffe2ad2d3ba30ba40f188285c1b91899a641ae1322aef4b20109b6a","tests/test_annotations.py":"7d9b144f2de95f3e5d1d4e577216d46899da50a635541e6b7931a07e036b9738","tests/test_arrays.py":"8675107a83b76aea5b295d7404e23f5134b200846f752d4d7c15d3c30ffabd4d","tests/test_chaining.py":"c93b4542579ad999f5d2fe5ff58cd4422ca14e2638b5fdd633e4da3ec87cfa23","tests/test_collections.py":"8d0f9fba53ae1e0e0d1f1e870bf73b03fe7867930568a3c3b95d516742387f63","tests/test_functions.py":"fc8b66c77e5b873c23e8dd5d5919c35a2ef839da4e671b68d5f49f315046158e","tests/test_numerical.py":"15e0e3061f501e102b1947329970a0f0d0e06c13001cabc18b92d688a529d002","tests/test_objects.py":"7d5ab65769c311fb97cbc38c4707c51b7262343ede4c3cd0414cd449330a143a","tests/test_predicates.py":"03c1e366375513356c188c96a081047bd76230ebd901dbc8a5c9b01088453e45","tests/test_strings.py":"adb155954a0993fb248a49c04e383123f936d97826e4198631b68ecc7e9e4727","tests/test_utilities.py":"b26ba4547bbfadb6970bf24055958fd2b9857b6f58135090a7a54117a06fc093","tox.ini":"cb9f938dc655e9397de6ccd6483f44485ced3df585367f0b68b84e9ce3c9d44e"}
JSON

%check
%{__python3} - "%{buildroot}%{_datadir}/python-pydash/original" "%{buildroot}%{python3_sitelib}" buildroot <<'PY'
import ast,hashlib,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile,xml.etree.ElementTree as ET
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text())
assert sys.version_info[:2]==(3,11) and len(manifest)==76
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%%{NAME}',str(p)],text=True)=='python-pydash'
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
    # actual upstream site-package relocation, all module doctests, original 100%% coverage gate.
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

%files
%license LICENSE.rst
%doc README.rst AUTHORS.rst CHANGELOG.rst
%{python3_sitelib}/pydash/
%{python3_sitelib}/pydash-*.dist-info/
%{_datadir}/python-pydash/

%changelog
* Tue Oct 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 8.1.0-1
- Initial package retaining full upstream default tests and original coverage100.
- Express unchanged MIT license through file metadata for setuptools68 compatibility.
