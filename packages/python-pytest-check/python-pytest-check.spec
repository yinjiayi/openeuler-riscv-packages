# SPDX-License-Identifier: Apache-2.0
Name:           python-pytest-check
Version:        3.0.1
Release:        1%{?dist}
Summary:        Pytest checks that report multiple failures per test
License:        MIT
URL:            https://github.com/okken/pytest-check
Source0:        python-pytest-check-3.0.1.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-hatchling
BuildRequires:  python3-wheel
BuildRequires:  python3-pytest >= 7.0.0
BuildRequires:  python3-packaging
Requires:       python3
Requires:       python3-pytest >= 7.0.0
Requires:       python3-packaging

%description
Report multiple failed checks per test without changing the original test suite.

%prep
%setup -q -n pytest-check-8f3e82acb0f570a568d07e7ffebdd8be135eec19
mkdir -p ../pytest-check-pristine
cp -a . ../pytest-check-pristine/

%build
SOURCE_DATE_EPOCH=315532800 %{__python3} -m pip wheel --no-deps --no-index --no-build-isolation --wheel-dir wheelhouse .

%install
%{__python3} -m pip install --no-deps --no-index --no-compile --root %{buildroot} --prefix %{_prefix} wheelhouse/*.whl
install -d %{buildroot}%{_datadir}/python-pytest-check/original
cp -a ../pytest-check-pristine/. %{buildroot}%{_datadir}/python-pytest-check/original/
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/python-pytest-check/python-pytest-check-3.0.1.tar.gz
cat > %{buildroot}%{_datadir}/python-pytest-check/original-files.json <<'JSON'
{".coveragerc": "8f5ece4e4572cb4f299132053e969ce08628ae33b401e688634b2a7ff0763d71", ".github/.deployment.md": "52ceecadde902c3a56b1d824dfa40d06aecde42a8063adfb93a9d99e828521b9", ".github/FUNDING.yml": "4cf56c9fb23b5f9e2af24d3a2e56d01e2f16af969e16466511772a87d585f65e", ".github/workflows/main.yml": "a513f21a22a492ad853ae800ba618552748e0784dccf4d29af7699583878b01c", ".github/workflows/publish-to-pypi.yml": "bdbe328198c985e92b2f2ec167c51439a136a40d06d375ca25a8e945a25b377f", ".gitignore": "4179cddd0a3ebfb6bb19701e6a2f3f2bd0414f640827395b4d77440704f86fff", "LICENSE.txt": "55e27c867a07c71e9860e90994a11d71be264d09d53540b2c3ce68378fb7721f", "README.md": "702ae83e3ceb615dcf94675e514d68aca79ef3bd02900f97e092d7e492074402", "changelog.md": "6ac4423da2addb8598af2cc9198a0731a10f7d8e1b480fc2d28c76c803e52576", "examples/logging_to_a_file/conftest.py": "4f4c16586c21071790527118913277314fde6ef0e40a8fbe26df152827b63beb", "examples/logging_to_a_file/test_file_logging.py": "9bd5956f249f7f326da785bb03c4240177a0afc3202a1c60bdffec826216243d", "examples/test_example_alt_names.py": "ec1d623fe432bbf4fe322a655f8501b5222503bbc486e26d8cd0152cb07dfc4e", "examples/test_example_any_failures.py": "8aab4664391812fe0ac499cb07359c9703ecf72d49a96f101a7ca2100b74e247", "examples/test_example_check_and_assert.py": "bd1c4d3c02a9b16d8a8a316d72656d2df532e2fbf5aa4c88080ece69c2c076c7", "examples/test_example_check_check.py": "bdee36688f03f5b283555b0a57c0e66e5c509d10feb2be071a3990f491faecc8", "examples/test_example_check_func_decorator.py": "00d7e9984707ecb452104d1dd3916c85eb854c0840342c39ac48636df409fdc1", "examples/test_example_check_func_xfail.py": "fe8c7d9a3f0862cd36462c19f85be1311311d554863c04ce1d9d6d44038719b5", "examples/test_example_check_not_in_test.py": "57323b837efccbe8489dca88a0eb7b4df3c1c00d257995ccb7c43eec46c58bd5", "examples/test_example_context_functions.py": "1d2099ed2c9814ce7dc3ed42e5383301b1a83925fe0b2f88bbf0b6ce253dbaaf", "examples/test_example_context_manager_fail.py": "2c2457a2cfeda56957715126ef3e19b15cfce01b99187cbc6b333971b37fcb55", "examples/test_example_context_manager_pass.py": "923e63adb6eb3ddcbc4d6e7fe88f52d95f6f94e797b3168f1526612420b8a318", "examples/test_example_context_manager_type.py": "7e7b0905c709fb5939b01b8a49224ae61f7f041948b2f7c704dc9b20f3ed0fd9", "examples/test_example_fail_func.py": "7ae582ab9074e882a75ee9245f3e33ad1471295ce9c4181fe2e8dd0493b1c3f7", "examples/test_example_fail_in_fixture.py": "97c647db0f17ebe43e9b6da0999863f713f722688ca13d0c4263a173f51e4d7c", "examples/test_example_fail_in_teardown_with_skip.py": "5a23f42fe0904aeb7dd480856736a3213c78d43992e3b81af0c768fb33d290c6", "examples/test_example_fail_in_thread.py": "5fd6764c788b0748519080c9541c615870470bed96b37c517fbb760849649ea1", "examples/test_example_functions_fail.py": "7eaba0ec8fc69b66683e38d409168f532da78b9ddfa546137bc300950d5c4a1d", "examples/test_example_functions_pass.py": "94cb047550d6f171794aaf5f29b7a4c592de5e97bb5ef30cdbbe11ab69078f1e", "examples/test_example_functions_xfail.py": "41147014ac58811b8b712e24f30723ccf6fcdf15aa532d278b21b4ffd722dbe6", "examples/test_example_helpers.py": "f985798100a1c50db6d3dbf616604a1a9d87905d40d0ac60a93ccf31d0d97a1a", "examples/test_example_httpx.py": "86edebdf0f15e8c220b1b3c3a679ec31213d88c07bc2f76f95dcad6d980f4291", "examples/test_example_locals.py": "a4612a07eaa73c8a760987a8024510ba7c107ff76f63f203db1e898b125883e4", "examples/test_example_logging.py": "c86cdcca09a07f625ebd5c8d5a55626d916c199fe9a98a79cf69ef54057340d4", "examples/test_example_loop.py": "6dfd0294ef3bfb5d01ae72f698e0218f4c814b5122266a9ba362b797f31e0969", "examples/test_example_maxfail.py": "194c16f09b47dbdf87c1313e17c1f2de90f3681bccd88b7ccb7041d3c3d4a91a", "examples/test_example_message.py": "53b43fc0c21eca2abfa8aa2a7ca823c234bfaef39c4f19c19d72bfd39324a86d", "examples/test_example_mix_checks_and_assertions.py": "495e8cd317d0836bdac98eaff6be4bd88e8dc883d3b88f51210565f32e3f95ef", "examples/test_example_multi.py": "5e2967e6177a6f8c4782be17c9eae7360ccf35caf11dd4dc15cf5c33e6b427ac", "examples/test_example_multi_check_raises.py": "f3157b18b50d4e9be99b53bc208f3c786e1e32214837d082910671f838d0e4d5", "examples/test_example_multiple_failures.py": "d7780391d13225d2333e0646d0b78522e81bec042898aeb3a291376409e192f1", "examples/test_example_mypy.py": "6e84bace3b9b1055833f4add186c57ba6faeab082de5bedd2e371aaa34927c3b", "examples/test_example_mypy_fail.py": "020b6b235994369dce95f24998e86aee35ef814efb46377cdc7ee190bed3b35a", "examples/test_example_non_assert_exceptions.py": "477ab94adc919b41cc4b06de18b384ea3db0ab3e36e9da3bc18fed1163418a4d", "examples/test_example_parallel_threads.py": "e64e55b1e6e8ace8c7f1fd866ccd376cf4c53a2d2152d8d407f0e09890e21a3f", "examples/test_example_pass_in_thread.py": "c822da141de117b26c0476866c9942cf3ab4d47f70acb0f560dcca45d2577198", "examples/test_example_raises.py": "bf18981250d1234fd7eaa879631a72806a292c456a9dc11e67eb93ab979592b9", "examples/test_example_simple.py": "c169117985583aa755d3d9b849327ac4a93c6eb853540590d3d131158a8c4dcd", "examples/test_example_speedup_funcs.py": "dfa4cdae5ed7e48fb9ed5106316ae95c4d495aa7c6f74cc89cb7e1abf05773f3", "examples/test_example_stop_on_fail.py": "16a95048f59662559bf50626c835ba9a65335faa72c578399a7706d28feb1b8a", "examples/test_example_summary.py": "a3d0174e39f85065e82a042f7a67def4e6e71783f420ab25b03128653d97a90c", "examples/test_example_tb_style.py": "a88967e45da8020a14650f7529d9a2644f93a0d5a24d87e42a44eb742d68a8db", "examples/test_example_traceback.py": "e5e525bdbbcc6d1bc0296a99501852ab4a3901c857e1691e99152732d43b594f", "examples/test_example_tracebackhide.py": "662823b77f3c693bf02919539a081ba76179ac5ed0170f5d0c26cd7b7b2f7586", "examples/test_example_xfail.py": "f04bfb6768ccbf59c9b9ffaa09e69f3cbb804d29b5e4c9e6d10168e7c07ffd3f", "pyproject.toml": "866375a6cf73081673cb5c068f8bf95b11bbaaf077fabaeae88f3323a46ebdca", "src/pytest_check/__init__.py": "82657defa9b411bff6eb3404d3333c881447868bec18bccc49982d1b6d473375", "src/pytest_check/__init__.pyi": "674984063db0cebe442634ca547bff1faca18fcece360579af8a103631d1e9a6", "src/pytest_check/check_functions.py": "d7b2554e088f5ab991b736b3692aed539e886639f1a0ee540fd96313b9a95ae7", "src/pytest_check/check_log.py": "516f7d10a127588e9fd32c9f423675a5bc51f2be54623db6053b50411442abfb", "src/pytest_check/check_raises.py": "c2066e35d7e7f72d259552a361a38b50ccdda9f332775aa075b691337ccafe59", "src/pytest_check/context_manager.py": "a3c0545ca93a3774a8cb89f90280cde3d35aaabb7cda8a99aa1110db505ad911", "src/pytest_check/plugin.py": "9b332ca06b5bb95006ea4280894dfb417e69dd9bc55701ebe3f81d44c1732ff8", "src/pytest_check/pseudo_traceback.py": "7a54d83f81c5fc98500ec85b0354ac5cdaefb3618940ea5896294a5a78743fd4", "src/pytest_check/py.typed": "e16f1596201850fd4a63680b27f603cb64e67176159be3d8ed78a4403fdb1700", "tests/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "tests/conftest.py": "37f95629648cd85191b23f7ad628cab05cbba135c62980aa7ed5353b29ab7047", "tests/markers.py": "d0ead4288873c811d076f204b46240540377ee1a7f132ec2e9124abc6b77038c", "tests/test_alt_names.py": "877045b92383571a7045cf98a5759a2bc096047aa46b0272fab56eb63874e706", "tests/test_any_failures.py": "1e29438d6c388be4bcced4662a9238c3ad694dd386fac0824f95be0a210592c0", "tests/test_check_and_assert.py": "7c899008deb413cf10e244df80e7761f1e9290fa3ef13992cc52700b0ab5e5a7", "tests/test_check_check.py": "cddfd3107aaec084bc212c4ff59b629058fa1d487ba2853b08b847333f1e0227", "tests/test_check_context_manager.py": "f75da6fe3dabedd8603cf626f81ad12b8e190c298d726067e7a4d203b28547c9", "tests/test_check_fixture.py": "c8126f3c2e015906660c3dd2b26d3bde95f826006909d751d8b629d4042e9871", "tests/test_check_func_decorator.py": "3aefa69605b4bf5e113281956643cda237bd76ed1de87db7c245f3ee410396d2", "tests/test_fail_func.py": "d233fe4c3ad76c98768aaed510b57f95368ab50abcd6c5ce906700f1a16f0c7d", "tests/test_fail_in_fixture.py": "0d2dd2b043969b2c78982c44e5fb1e91341f3bfef586b1a187e822b6647548ef", "tests/test_fail_in_teardown_with_skip.py": "e05537bd5613c7d7c6dc5a3ace4dca9ab3cd708bbeda40a89c2328289fa65379", "tests/test_func_xfail.py": "6294173d0d2999ad965a7a8bd1bf59f90f89f0a84509cdd2b579a176cec66a44", "tests/test_functions.py": "2fa33b3cd89218b92c9ee95201400125f4deec1ca4c2bdf0183dfb62fdc4eb25", "tests/test_helpers.py": "0c1d487c578987b4a9736f2a370096c0f67bd3a957c59818f1732e9d6cabc841", "tests/test_locals.py": "09494dee0d90d8ee33d04620a668e8c6bac748186b4ad45944bf8dd17c84309e", "tests/test_logging.py": "f4f43dccca0235b43c361bc2901b1461b7985784a7a30552b2d085195d52c8fd", "tests/test_maxfail.py": "75943d5a4951a492bdd450f4ca4de18363b37c055da97bb9b842b64347bda840", "tests/test_message.py": "e062b490fe38401ec82f39808fecce1cf1597c0aee62d5084b807b6ab5a327ca", "tests/test_non_assert_exceptions.py": "7568b3b10d1b454cae04a26cb12833266d574b19d1d7add0f9584bcde422158b", "tests/test_not_in_test.py": "5d56ca7bd12d8e19a31d485fa5f02c796458cdf6ed10ad148bc5e3f2b673b593", "tests/test_parallel_threads.py": "960272b7711c801f492a4b65c2f286767d4c2ffe486181dfb4f69b38e752624f", "tests/test_pseudo_tb_corner_cases.py": "92fddc5e100f9d70baa00276a097784c3437255c7d7e0c9c878d927a47c07fd8", "tests/test_raises.py": "dc2106e7bc3010b21e41da7d8fb0bc6df99cd431166ce08a0575c1ccc6b1bdd3", "tests/test_red.py": "e316be5d23cb512f788cb5e932274b7a30b3c7e88ee362b409bdc82527cdba82", "tests/test_reportlog.py": "0bf7954ee7d90b5d3fd24f1257da9248d98a1c55f0f067464a28af9676473a80", "tests/test_speedup_flags.py": "3ceff6a9a1a11039af9069b28c5a4e09cfecd91a5ea5a501819f40779065e30e", "tests/test_speedup_functions.py": "f8d48ce952d90c6fc74bb813aa06590d2b6ac2238f4857021f35d91a95dc0d9d", "tests/test_stop_on_fail.py": "17bd38d5e289d783a254847ad083e42912a3b778b5adc7b08c81c4aebd224fe8", "tests/test_summary.py": "dd19f3be807fc79a50818596ea70ebd0165935416c6d824675a15b4567f4e05f", "tests/test_tb_line.py": "3aff35691edf4d7704c425a589099d9eef8b18b8d76a39bc7bba0f6ee6ba2e61", "tests/test_tb_style.py": "c086c0ee8c94a0167f96c650732f0403a3fec9b8acec6f06b7841a7e95368922", "tests/test_thread.py": "a31eb7e7522ecf32f8ac11ef47f6d3fb8e00510b57ffda56f852fb1906c234ad", "tests/test_thread_runner_compat.py": "b6c2654871ae04c3b05158ccc53641a71d3b4c75f13d7fd4eb8c7f3ef95093ab", "tests/test_tracebackhide.py": "63f4438769925b5be4c9686820ed07ca1d3f5414e71c9dbda0f55ff348df92ff", "tests/test_xfail.py": "5de7bc03f4743592fa6dbfe23cea33a6c3a021276a6f1f483f1ed1d51c5438ea", "tox.ini": "65d104b8bc853b7c23d29cb126a7f8abed38e6186a10f8f5435934eda882814c"}
JSON

%check
env -u PYTHONHOME -u PYTHONSTARTUP -u COVERAGE_PROCESS_START -u PYTEST_ADDOPTS -u PYTEST_PLUGINS -u PYTHONPATH %{__python3} - "%{buildroot}%{_datadir}/python-pytest-check/original" "%{buildroot}%{python3_sitelib}" buildroot <<'PY'
import hashlib,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text());runtime={p.removeprefix('src/pytest_check/'):h for p,h in manifest.items() if p.startswith('src/pytest_check/')}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%%{NAME}',str(p)],text=True)=='python-pytest-check'
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

%files
%license LICENSE.txt
%doc README.md changelog.md
%{python3_sitelib}/pytest_check/
%{python3_sitelib}/pytest_check-*.dist-info/
%{_datadir}/python-pytest-check/

%changelog
* Tue Oct 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.1-1
- Fixed official source and intact core defaults with RPM-owned entrypoint checks.
