# SPDX-License-Identifier: Apache-2.0
Name:           python-click-log
Version:        0.4.0
Release:        1%{?dist}
Summary:        Logging integration for Click applications
License:        MIT
URL:            https://github.com/click-contrib/click-log
Source0:        python-click-log-0.4.0.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-pytest
BuildRequires:  python3-click
Requires:       python3
Requires:       python3-click
Requires:       python3-pytest

%description
Integrate logging with Click while preserving the original core test suite.

%prep
%setup -q -n click-log-f84e0944ce78227ed1b3f095534e89a968d13dc2
mkdir -p ../click-log-pristine
cp -a . ../click-log-pristine/

%build
SOURCE_DATE_EPOCH=315532800 %{__python3} -m pip wheel --no-deps --no-index --no-build-isolation --wheel-dir wheelhouse .

%install
%{__python3} -m pip install --no-deps --no-index --no-compile --root %{buildroot} --prefix %{_prefix} wheelhouse/click_log-0.4.0-*.whl
install -d %{buildroot}%{_datadir}/python-click-log/original
cp -a ../click-log-pristine/. %{buildroot}%{_datadir}/python-click-log/original/
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/python-click-log/python-click-log-0.4.0.tar.gz
cat > %{buildroot}%{_datadir}/python-click-log/original-files.json <<'JSON'
{".github/workflows/tests.yml": "0e713db29a1bd08c02ac2fa93c9c011dad6deba26561ea4eb1845de53826d76f", ".gitignore": "ed093f361312dadcd26c4f251d617eaf51b1ebfa71d12178c999a259bf7001c5", "LICENSE": "cd55eccfe4c90e57f372446b50292ad550a4bfcc3534af8942fb8ca5c19d423e", "MANIFEST.in": "8c1ed106e2d702ad5eda2fee0a898b5230ddf813bf94aa995e85f92dea06df65", "Makefile": "2586a30de31a1534232f05e176cf548fdddae0fa61b50115c3f06cbe42c6c79b", "README.rst": "8587c8c1a46d75a0d65f2ca34619a8a4cc6c075e25e59d68899827817f1c7cbc", "click_log/__init__.py": "4b5195b738d90ba11ac4d8d18e35568dbf5da73aee6e50fedb56275608d06be7", "click_log/core.py": "6afe21791b4568f8b02cc73033346b2c7baf925a2bb745e6169e566c72ba63fe", "click_log/options.py": "f43257e88b84c02348babf32bb00a063aa7c95fa97998b6094c46b959f65ae57", "docs/Makefile": "15ffea31e332411f8a4663f2c24b8e5156f2e9d339cb4f5990c5199155f5f8ab", "docs/conf.py": "3414e21c10ffb19f6566a92d8de2dd64bc9321ff9c75a8dd2c9a23c451115a6b", "docs/index.rst": "4b5e6dda22a7f1f10ae26419b79eb943154df0c28af4ab63546ec54a86229cc1", "docs/make.bat": "fe7032c1cacbb62623dd28bb039d4c2487a7cebadd713468fde3afc11c2783dc", "setup.cfg": "c4c690665ef87baf37f4e7100d4c150bd1974c5bbfeb3b3594eee75ea536437f", "setup.py": "600ae0244bcb845d7fd3cbdaea33182e20aa2d3bca9b50e6c58ebc56aa42c9fd", "tests/test_basic.py": "1debe0f4bcd28baae4d6852e7d00cbf7082804fb82e0444e33fc372b99ba7b4a", "tox.ini": "6ebcbeccfae5c5cfa7cc45178460a4f8c8231368c1ab6877caa554d27804d675"}
JSON

%check
env -u PYTHONHOME -u PYTHONSTARTUP -u COVERAGE_PROCESS_START -u PYTEST_ADDOPTS -u PYTEST_PLUGINS -u PYTHONPATH %{__python3} - "%{buildroot}%{_datadir}/python-click-log/original" "%{buildroot}%{python3_sitelib}" buildroot <<'PY'
import hashlib,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text());runtime={p:h for p,h in manifest.items() if p.startswith('click_log/') and p.endswith('.py')}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%%{NAME}',str(p)],text=True)=='python-click-log'
assert len(manifest)==17 and len(runtime)==3
for p,h in manifest.items():
    q=original/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
for p,h in runtime.items():
    q=site/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
for p in (site/'click_log').rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(site).as_posix()
    if rel not in runtime:assert p.parent.name=='__pycache__' and p.suffix=='.pyc' and any(p.name.startswith(pathlib.Path(x).stem+'.') and p.parent.parent==site/pathlib.Path(x).parent for x in runtime),rel
    owned(p)
archive=original.parent/'python-click-log-0.4.0.tar.gz';assert digest(archive)=='e74dca8612d5e3a64fe4cf2d80b2b746b9b3ed29349f56b78068d244849e798c';owned(archive);owned(original.parent/'original-files.json')
for p in original.rglob('*'):
    if p.is_file() and p.relative_to(original).as_posix() not in manifest:assert p.parent.name=='__pycache__' and p.suffix=='.pyc' and any(p.name.startswith(pathlib.Path(x).stem+'.') and p.parent.parent==original/pathlib.Path(x).parent for x in manifest if x.endswith('.py'))
guard="""import hashlib,importlib.abc,importlib.machinery,importlib.metadata,json,os,pathlib,sys
site=pathlib.Path(SITE_JSON).resolve();expected=HASH_JSON
def fail_closed():os._exit(86)
if sys.version_info[:2]!=(3,11) or any(n=='click_log' or n.startswith('click_log.') for n in sys.modules):fail_closed()
try:
    if importlib.metadata.version('click')!='8.1.7' or importlib.metadata.version('pytest')!='7.4.4':fail_closed()
except BaseException:fail_closed()
class OriginGuard(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname=='click_log' or fullname.startswith('click_log.'):
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
    import click_log
    p=pathlib.Path(click_log.__file__).resolve()
    if p!=site/'click_log/__init__.py' or click_log.__version__!='0.4.0':fail_closed()
    print(json.dumps({'guarded_runtime_origin':str(p),'runtime_sha256':expected,'python':list(sys.version_info[:3]),'click':importlib.metadata.version('click'),'pytest':importlib.metadata.version('pytest')}),file=sys.stderr)
except BaseException:fail_closed()
""".replace('SITE_JSON',repr(str(site))).replace('HASH_JSON',repr(runtime))
with tempfile.TemporaryDirectory(prefix='python-click-log-defaults-') as scratch:
    work=pathlib.Path(scratch)/'original';work.mkdir()
    for p in manifest:
        if p.startswith('click_log/'):continue
        dst=work/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/p,dst)
    assert not (work/'click_log').exists()
    env=dict(os.environ)
    for key in ('PYTHONHOME','PYTHONSTARTUP','COVERAGE_PROCESS_START','PYTEST_ADDOPTS','PYTEST_PLUGINS'):env.pop(key,None)
    env.update(PYTHONPATH=str(site),PYTHONDONTWRITEBYTECODE='1',PYTHONNOUSERSITE='1')
    code=guard+'\nd=importlib.metadata.distribution("click-log");assert d.version=="0.4.0";p=pathlib.Path(d._path).resolve();p.relative_to(site);print(str(p))\n'
    metadata=pathlib.Path(subprocess.check_output([sys.executable,'-c',code],cwd=work,env=env,text=True).strip())
    for p in metadata.rglob('*'):
        if p.is_file():owned(p)
    # Exact original core testenv command: python -m pytest {posargs}, empty posargs.
    code=guard+'\nimport runpy\nsys.argv=["pytest"]\nrunpy.run_module("pytest",run_name="__main__")\n'
    subprocess.run([sys.executable,'-c',code],cwd=work,env=env,check=True)
    for p,h in manifest.items():assert digest(original/p)==h
    for p,h in runtime.items():assert digest(site/p)==h
    print(json.dumps({'route':'Original core testenv python -m pytest, empty posargs on explicitly new target CPython3.11/distro Click8.1.7','original_files':17,'runtime_files':3,'original_commands':[['python','-m','pytest']],'runtime_origin':str(site/'click_log'),'engine':'installed-RPM' if installed else 'buildroot-wheel','boundary':'All6 original tests/assertions/config retained, no filter/new skip/pin relaxation. Original tox rolling GitClick bootstrap and legacy3.7-3.10/PyPy environments, docs/lint/release upload remain preserved but unclaimed.'}))
PY

%files
%license LICENSE
%doc README.rst
%{python3_sitelib}/click_log/
%{python3_sitelib}/click_log-*.dist-info/
%{_datadir}/python-click-log/

%changelog
* Tue Oct 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.0-1
- Fixed official source and intact original defaults with installed origin guards.
