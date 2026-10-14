# SPDX-License-Identifier: Apache-2.0
Name:           python-click-aliases
Version:        1.0.7
Release:        1%{?dist}
Summary:        Aliases for Click groups and commands
License:        MIT
URL:            https://github.com/click-contrib/click-aliases
Source0:        python-click-aliases-1.0.7.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-poetry-core
BuildRequires:  python3-wheel
BuildRequires:  python3-pytest >= 7.4.2
BuildRequires:  python3-pytest < 8
BuildRequires:  python3-click >= 8.1.7
BuildRequires:  python3-click < 9
Requires:       python3
Requires:       python3-click >= 8.1.7
Requires:       python3-click < 9
Requires:       python3-pytest >= 7.4.2
Requires:       python3-pytest < 8

%description
Provide aliases for Click groups and commands with the full original test suite.

%prep
%setup -q -n click-aliases-8341453c076dc616cd6e02aeaae13e2be73a46af
mkdir -p ../click-aliases-pristine
cp -a . ../click-aliases-pristine/

%build
SOURCE_DATE_EPOCH=315532800 %{__python3} -m pip wheel --no-deps --no-index --no-build-isolation --wheel-dir wheelhouse .

%install
%{__python3} -m pip install --no-deps --no-index --no-compile --root %{buildroot} --prefix %{_prefix} wheelhouse/click_aliases-1.0.7-*.whl
install -d %{buildroot}%{_datadir}/python-click-aliases/original
cp -a ../click-aliases-pristine/. %{buildroot}%{_datadir}/python-click-aliases/original/
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/python-click-aliases/python-click-aliases-1.0.7.tar.gz
cat > %{buildroot}%{_datadir}/python-click-aliases/original-files.json <<'JSON'
{".github/workflows/python-publish.yml": "e4bb67ba1c3d4debe1ce77650667548183274bbdf1100c52c9dd6ef031dd9f9b", ".github/workflows/tests.yml": "91b47dc8915ec108ab3f342317e3fa535684504d112a785e25a7ee2e18744231", ".gitignore": "f3b7b405d0673dc92f90cdf988254368b4fded5b901ec2404788ce74cb124df2", ".travis.yml": "982cdb6bc499ea7fabc0e38fae6ba275600a76ba4ac0e4e4cb04fb5e5e405f63", "LICENSE": "e3b4a4c21dc9d032a590e903dc5cc0b9404e952821bb36e88916b4858abacfa8", "MANIFEST.in": "21b6e04071be2847dd7a98ceaf3d362d55e18f990ed798375ab787495688e526", "README.md": "37be819391b8bfadd9a1d608a2c1b265f6c3b08d546bacc1164b7676318db88e", "click_aliases/__init__.py": "e3b2a2ab4f79d5bea78365a1745358a07c3242d8ffe32746713a9bd8edcf98e0", "click_aliases/py.typed": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "examples/bar/subcommand.py": "f251aec16b6a9459fd8ccfb4fc3e06b445c78de03164bfdfae98faacbb2867bd", "examples/foo.py": "16c5f885945033d62de7258769644f6be8d12bb6821d1033e125b84f0870f8de", "examples/foobar.py": "7dfbb4fe71e92cd0abc8b9cb024b2e1a048eebbc21387e79d1126523a86e7f88", "examples/naval.py": "bec95dbf6be646d564dc88ea592472c90e9ea6190ff274cfc43e914e487c179c", "poetry.lock": "cf083f175f18160dadd99d7baa76210e69f718debf82d3ef1253121ba0dc74f9", "pyproject.toml": "a04c478b93dd2f9688fea8c2cf0bf7c4281d0e6cf37ef7eaf14fbf671032a21a", "setup.cfg": "78a84014cdc83d884f629d75d03c9c78c57b5159f3b4a9876573ff333d42b9a3", "setup.py": "61059660c1484022614410492d9c3e66d93152555dbc7bb25f0c62083cc72329", "tests/test_basic.py": "789984e4b412ffb44f668b115fec6a117978211b657ba3a7b58193ef0cdebefe", "tests/test_foobar.py": "d81f89fb8eea317456cab37e24dd7f993e7ebbfeb3cfa46fc9cd1bc3eb8a94f5", "tests/test_naval.py": "62c44441673b30ae10367c2d7d7fabc1fa226c36eaf9b9ddc95438c1d4ba36fb", "tox.ini": "2149e25f370558163355417cd2777a31073380b1be955cc2c1a0bd4922b53b91"}
JSON

%check
env -u PYTHONHOME -u PYTHONSTARTUP -u COVERAGE_PROCESS_START -u PYTEST_ADDOPTS -u PYTEST_PLUGINS -u PYTHONPATH %{__python3} - "%{buildroot}%{_datadir}/python-click-aliases/original" "%{buildroot}%{python3_sitelib}" buildroot <<'PY'
import hashlib,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text());runtime={p:h for p,h in manifest.items() if p.startswith('click_aliases/') and p in ('click_aliases/__init__.py','click_aliases/py.typed')}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%%{NAME}',str(p)],text=True)=='python-click-aliases'
assert len(manifest)==21 and len(runtime)==2
for p,h in manifest.items():
    q=original/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
for p,h in runtime.items():
    q=site/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
for p in (site/'click_aliases').rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(site).as_posix()
    if rel not in runtime:assert p.parent.name=='__pycache__' and p.suffix=='.pyc' and any(p.name.startswith(pathlib.Path(x).stem+'.') and p.parent.parent==site/pathlib.Path(x).parent for x in runtime if x.endswith('.py')),rel
    owned(p)
archive=original.parent/'python-click-aliases-1.0.7.tar.gz';assert digest(archive)=='51866180740c4ead2c9b73da9347ec48932bd1e2a9104d534bda110259c87c74';owned(archive);owned(original.parent/'original-files.json')
for p in original.rglob('*'):
    if p.is_file() and p.relative_to(original).as_posix() not in manifest:assert p.parent.name=='__pycache__' and p.suffix=='.pyc' and any(p.name.startswith(pathlib.Path(x).stem+'.') and p.parent.parent==original/pathlib.Path(x).parent for x in manifest if x.endswith('.py'))
guard="""import hashlib,importlib.abc,importlib.machinery,importlib.metadata,json,os,pathlib,sys
site=pathlib.Path(SITE_JSON).resolve();expected=HASH_JSON
def fail_closed():os._exit(86)
if sys.version_info[:2]!=(3,11) or any(n=='click_aliases' or n.startswith('click_aliases.') for n in sys.modules):fail_closed()
try:
    if importlib.metadata.version('click')!='8.1.7' or importlib.metadata.version('pytest')!='7.4.4':fail_closed()
except BaseException:fail_closed()
class OriginGuard(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname=='click_aliases' or fullname.startswith('click_aliases.'):
            try:
                spec=importlib.machinery.PathFinder.find_spec(fullname,path)
                if not spec or not spec.origin:fail_closed()
                p=pathlib.Path(spec.origin).resolve();rel=p.relative_to(site).as_posix()
                if rel not in expected or hashlib.sha256(p.read_bytes()).hexdigest()!=expected[rel]:fail_closed()
                return spec
            except BaseException:fail_closed()
        return None
sys.meta_path.insert(0,OriginGuard())
try:
    import click_aliases
    p=pathlib.Path(click_aliases.__file__).resolve()
    if p!=site/'click_aliases/__init__.py':fail_closed()
    print(json.dumps({'guarded_runtime_origin':str(p),'runtime_sha256':expected,'python':list(sys.version_info[:3]),'click':importlib.metadata.version('click'),'pytest':importlib.metadata.version('pytest')}),file=sys.stderr)
except BaseException:fail_closed()
""".replace('SITE_JSON',repr(str(site))).replace('HASH_JSON',repr(runtime))
with tempfile.TemporaryDirectory(prefix='python-click-aliases-defaults-') as scratch:
    work=pathlib.Path(scratch)/'original';work.mkdir()
    for p in manifest:
        if p.startswith('click_aliases/'):continue
        dst=work/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/p,dst)
    assert not (work/'click_aliases').exists()
    env=dict(os.environ)
    for key in ('PYTHONHOME','PYTHONSTARTUP','COVERAGE_PROCESS_START','PYTEST_ADDOPTS','PYTEST_PLUGINS'):env.pop(key,None)
    env.update(PYTHONPATH=str(site),PYTHONDONTWRITEBYTECODE='1',PYTHONNOUSERSITE='1')
    code=guard+'\nd=importlib.metadata.distribution("click-aliases");assert d.version=="1.0.7";p=pathlib.Path(d._path).resolve();p.relative_to(site);print(str(p))\n'
    metadata=pathlib.Path(subprocess.check_output([sys.executable,'-c',code],cwd=work,env=env,text=True).strip())
    for p in metadata.rglob('*'):
        if p.is_file():owned(p)
    # Exact original current GHA command: python -m pytest, no additional arguments.
    code=guard+'\nimport runpy\nsys.argv=["pytest"]\nrunpy.run_module("pytest",run_name="__main__")\n'
    subprocess.run([sys.executable,'-c',code],cwd=work,env=env,check=True)
    for p,h in manifest.items():assert digest(original/p)==h
    for p,h in runtime.items():assert digest(site/p)==h
    print(json.dumps({'route':'Original GHA CPython3.11 command python -m pytest on distribution Click8.1.7/pytest7.4.4','original_files':21,'runtime_files':2,'original_commands':[['python','-m','pytest']],'runtime_origin':str(site/'click_aliases'),'engine':'installed-RPM' if installed else 'buildroot-wheel','boundary':'All9 original tests/assertions/config retained, no filter/new skip/pin relaxation. Legacy tox/Travis interpreter and Click5-7 matrices plus developer Poetry lock and lint/coverage/publish routes remain preserved but unclaimed.'}))
PY

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/click_aliases/
%{python3_sitelib}/click_aliases-*.dist-info/
%{_datadir}/python-click-aliases/

%changelog
* Wed Oct 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.7-1
- Fixed official source and intact original defaults with installed origin guards.
