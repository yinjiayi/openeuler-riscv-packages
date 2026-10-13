# SPDX-License-Identifier: Apache-2.0
Name:           python-dotty-dict
Version:        1.3.1
Release:        1%{?dist}
Summary:        Dictionary wrapper for quick access to deeply nested keys
License:        MIT
URL:            https://github.com/pawelzny/dotty_dict
Source0:        python-dotty-dict-1.3.1.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-poetry-core >= 1.0.0
BuildRequires:  python3-pytest
Requires:       python3
Requires:       python3-pytest

%description
Dotty wraps dictionaries and exposes deeply nested keys through dot notation.

%prep
%setup -q -n dotty_dict-74c527265e56a46a2485561fbc74646a063df5da
mkdir -p ../dotty-pristine
cp -a . ../dotty-pristine/

%build
SOURCE_DATE_EPOCH=315532800 %{__python3} -m pip wheel --no-deps --no-index --no-build-isolation --wheel-dir wheelhouse .

%install
%{__python3} -m pip install --no-deps --no-index --no-compile --root %{buildroot} --prefix %{_prefix} wheelhouse/dotty_dict-1.3.1-*.whl
install -d %{buildroot}%{_datadir}/python-dotty-dict/original
cp -a ../dotty-pristine/. %{buildroot}%{_datadir}/python-dotty-dict/original/
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/python-dotty-dict/python-dotty-dict-1.3.1.tar.gz
cat > %{buildroot}%{_datadir}/python-dotty-dict/original-files.json <<'JSON'
{".bumpversion.cfg":"6db12d99d32bbdc2f0e9a5a8aec507108c50f15a384dccf14c44ce8fcd3ba293",".circleci/config.yml":"fa3f24333ce6afc4c733f65b514bc8b2f2ff4033b2e5083c38bf34794fe5ad5f",".editorconfig":"6d5d61e25d429ca791b62f0e63e49ee22877447e746ed645e461d774264d1340",".gitignore":"b42e4b3d0a157a8fff7f97de7d49c7480a4b8516c85cd546ddd6b927e388c0c8","AUTHORS.rst":"d637a99a0030a7419f642307e4f1e3d043d54b1e3a655b0f3333225abdd6eea0","CONTRIBUTING.rst":"3e76c9c61c9cef0111c662834603cc792b157a6db734d88e929f734c29984ca5","LICENSE":"2009f4a57f95ce8aa76b76421bb7da6679eace67d5c10118edc692ecc41dc62b","MANIFEST.in":"280ae7122350b605033f7b01b945d53e4e980fd16dceb3a3d2ff8c0e6a746588","Makefile":"7df2aa305c0c9236d0fb98afd0f2934a9692af3f300de779d6037f13f69bb6a0","README.rst":"2783c1182efce9063ca93dad8d0ef526c5bd261a2bc898b38507d47fb0a86581","docs/Makefile":"2270360b15b5d6556a54a81fc833685bea70598cd9fc5ce3016e39506fe96f85","docs/_static/.gitkeep":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","docs/_templates/layout.html":"8519579b64c7d0b0139a04d7546d14bbef8b53ee79d50193468653923304da09","docs/api.rst":"a3c61a57610d9fe59741a9813d91b8a9ffff4c72087b700c41dc5d52753d8660","docs/authors.rst":"0ba8e9a403475ae12773cfce9fc7a32bce591e9801a1adde71927982f51d901b","docs/conf.py":"3f64e960fae364600cd12b89224ac8e04f09498109bfdde12cf2c39e2d4e70d4","docs/contributing.rst":"87d5c7434971ff248a817426c2a84940b3c3ed51251ddcaed6bb8a7d85afad80","docs/dotty_dict.rst":"087bcb5ee8cba1da1fa14d6e312f7bcdb88b38413041aca1eff5fc1084e3a93f","docs/examples.rst":"f4fdd3be2b876ccc5695782a4ed651425a38e01fdc1f7d93802f1b349af6417d","docs/index.rst":"49ec1a12bd078a1348a99a3121019063063b6329c808dd6216fb10d6e7d64932","dotty_dict/__init__.py":"e2c9058ffb1da37dd25aa4de7d5d49040bd9893e0c63fa41e726912f90cc355b","dotty_dict/dotty_dict.py":"e44241e233aa33fe0e255d99fc739204af1942f710b6faf070a728f4170532e4","example/__init__.py":"4aaf57bafc72d96575eba6b9889363857ad91d6969ddecc187e281bd10eed8bb","example/advanced.py":"0a52536f219ded35907b6d56f62b7a11a8ebcc9bafb98ad3c134f26148da21a6","example/basics.py":"1e31c41ba2564a0999fab84b85398589cf4bc59d1573c8adc5a576a11ceaa7cf","example/customization.py":"2d734c4ec2b7664c3de42010daa7f2cfcd34e3c47c35ceadd01a9820f2822989","poetry.lock":"a6f5699f8fc952ab00c88a1b409a2c930aeef7258e33e7e744354fb3346c1acc","pyproject.toml":"c05c63b3e9da133126cc681d41dd46328d34bb6d4de3462a2af02b6f2343b8c6","setup.py":"48e27fe7898d3da65040f8503e673ca3b9c710f964b158f6b66b68c5a89afd15","tests/__init__.py":"8b084a9f378124b2b1a51563bf3c22444eb7ff33692017da28b2136ae56987ed","tests/test_dotty_api.py":"901386e7aa6c1201214603d63d5018cf79f7d07f99e008f00d58c5ac388b9d4a","tests/test_dotty_basics.py":"4e34bfc8a47a6300a22f37c758c70f4703fd35c16267a222bbae41c85970588e","tests/test_dotty_cache.py":"9c07fe4751785487b629350e6bb6c2d52ab938aeeb27a3bd1e24e6ae2febf379","tests/test_dotty_value_access.py":"5889944814604fe13b11eefeb20b9e446a5415d551dd300c389fb478f9076c19","tests/test_examples.py":"c2055e0a205162bea886a9e58576f51bf4f50fc90bface9e6145f988de8bf586","tests/test_list_in_dotty.py":"15111c296a7d3e3e3a8b83135bab962f6d7f9853a1491ea9b63a1c18087bdf59","tox.ini":"93b2249779191980878ff1e5aa5641b0f3ff85ba9ed7d5a445953d6c70f3e0d9"}
JSON

%check
%{__python3} - "%{buildroot}%{_datadir}/python-dotty-dict/original" "%{buildroot}%{python3_sitelib}" buildroot <<'PY'
import hashlib,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text())
assert sys.version_info[:2]==(3,11) and len(manifest)==37
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%%{NAME}',str(p)],text=True)=='python-dotty-dict'
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

%files
%license LICENSE
%doc README.rst AUTHORS.rst
%{python3_sitelib}/dotty_dict/
%{python3_sitelib}/dotty_dict-*.dist-info/
%{_datadir}/python-dotty-dict/

%changelog
* Tue Oct 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.1-1
- Initial package preserving all37 originals and full79 core tests/examples.
