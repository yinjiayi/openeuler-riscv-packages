# SPDX-License-Identifier: Apache-2.0
Name:           python-pytest-instafail
Version:        0.5.0
Release:        1%{?dist}
Summary:        Show pytest failures immediately
License:        BSD-3-Clause
URL:            https://github.com/pytest-dev/pytest-instafail
Source0:        python-pytest-instafail-0.5.0.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-pytest
BuildRequires:  python3-pexpect
BuildRequires:  python3-pytest-xdist
Requires:       python3
Requires:       python3-pytest >= 5
Requires:       python3-pexpect
Requires:       python3-pytest-xdist

%description
A pytest plugin that reports failure and error details immediately.
The complete original test/configuration corpus is retained for installation QA.

%prep
%setup -q -n pytest-instafail-aab3a1e8f899584b9b31a56daf9f61cdc206a088
mkdir -p ../instafail-pristine
cp -a . ../instafail-pristine/

%build
SOURCE_DATE_EPOCH=315532800 %{__python3} -m pip wheel --no-deps --no-index --no-build-isolation --wheel-dir wheelhouse .

%install
%{__python3} -m pip install --no-deps --no-index --no-compile --root %{buildroot} --prefix %{_prefix} wheelhouse/*.whl
install -d %{buildroot}%{_datadir}/python-pytest-instafail/original
cp -a ../instafail-pristine/. %{buildroot}%{_datadir}/python-pytest-instafail/original/
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/python-pytest-instafail/python-pytest-instafail-0.5.0.tar.gz
cat > %{buildroot}%{_datadir}/python-pytest-instafail/original-files.json <<'JSON'
{".github/workflows/test.yml":"82a3249014bfb5b874fe05e1973e2e4c147384f3e1a60722c10396b856d8cda2",".gitignore":"ac7b26ebf80a8816353171867cb67be6acc1035419ed51976b77691ddb4e0844","CHANGES.rst":"7d71b923e1e234d695b9918603952784b2042f3b113179e3d65014d1a63f54a2","LICENSE":"45f321ed084adee02dec233ca9704de5a88a07ca2ffe42c3784944fa6d4b0786","MANIFEST.in":"4cc98acc0a70ea5fe18968fbe10f492af8259c3ce5b610adcf5df0f6d391d77c","README.rst":"08a40977571cd5369112280f739caa5dd86dad51601f5071d559f97207bfaa4a","pytest_instafail.py":"3a629075e4c0a3279c9b6ea5ac6be4777dbf5028f980353dbb80bb0da641d2e1","setup.cfg":"d7792e8b22f76a3beaea29375de01fed6115f0cce94214b7e991deb7d43d7e28","setup.py":"d256e805f9f0f90b86b53b3aad05f56b21d3704d53f1759a9dfda2d782d55b17","test_instafail.py":"934c68027b39fa570335e482f5d5823ce5b4a3e58d19d6f8e625e328bf06bb53","tox.ini":"458e603f46eff9673ab5d5718b7ba8711752cc550a3a95075fa796364d6d3264"}
JSON

%check
env -u PYTHONHOME -u PYTHONSTARTUP -u COVERAGE_PROCESS_START -u PYTEST_ADDOPTS -u PYTEST_PLUGINS -u PYTEST_DISABLE_PLUGIN_AUTOLOAD -u PYTHONPATH %{__python3} - "%{buildroot}%{_datadir}/python-pytest-instafail/original" "%{buildroot}%{python3_sitelib}" buildroot <<'PY'
import hashlib,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text())
runtime_hash='3a629075e4c0a3279c9b6ea5ac6be4777dbf5028f980353dbb80bb0da641d2e1'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%%{NAME}',str(p)],text=True)=='python-pytest-instafail'
assert len(manifest)==11 and manifest['pytest_instafail.py']==runtime_hash
for p,h in manifest.items():
    q=original/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
module=site/'pytest_instafail.py';assert module.is_file() and not module.is_symlink() and digest(module)==runtime_hash;owned(module)
archive=original.parent/'python-pytest-instafail-0.5.0.tar.gz'
assert digest(archive)=='f8de1f7e72ae7fd23d46dd60863ac4b26d6d3531715c44ca4c6ed40b98d7bf5a';owned(archive);owned(original.parent/'original-files.json')
assert digest(original/'LICENSE')=='45f321ed084adee02dec233ca9704de5a88a07ca2ffe42c3784944fa6d4b0786'
for p in original.rglob('*'):
    if p.is_file():assert p.relative_to(original).as_posix() in manifest;owned(p)
guard="""import hashlib,importlib.abc,importlib.machinery,os,pathlib,sys
expected=pathlib.Path(SITE_JSON)/'pytest_instafail.py'
def fail_closed():os._exit(86)
if 'pytest_instafail' in sys.modules:fail_closed()
class OriginGuard(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname=='pytest_instafail':
            try:
                spec=importlib.machinery.PathFinder.find_spec(fullname,path)
                if not spec or not spec.origin:fail_closed()
                p=pathlib.Path(spec.origin).resolve()
                if p!=expected or hashlib.sha256(p.read_bytes()).hexdigest()!=RUNTIME_JSON:fail_closed()
                print('guarded_instafail_runtime='+str(p),file=sys.stderr)
                return spec
            except BaseException:fail_closed()
        return None
sys.meta_path.insert(0,OriginGuard())
""".replace('SITE_JSON',repr(str(site))).replace('RUNTIME_JSON',repr(runtime_hash))
with tempfile.TemporaryDirectory(prefix='python-pytest-instafail-defaults-') as scratch:
    base=pathlib.Path(scratch);work=base/'original';work.mkdir();guards=base/'guard';guards.mkdir()
    for p in manifest:
        if p=='pytest_instafail.py':continue
        dst=work/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/p,dst)
    assert not (work/'pytest_instafail.py').exists()
    (guards/'sitecustomize.py').write_text(guard)
    env=dict(os.environ)
    for key in ('PYTHONHOME','PYTHONSTARTUP','COVERAGE_PROCESS_START','PYTEST_ADDOPTS','PYTEST_PLUGINS','PYTEST_DISABLE_PLUGIN_AUTOLOAD','PYTHONPATH'):env.pop(key,None)
    env.update(PYTHONPATH=str(guards)+os.pathsep+str(site),PYTHONDONTWRITEBYTECODE='1',FORCE_COLOR='1')
    code="import importlib.metadata,pathlib;d=importlib.metadata.distribution('pytest-instafail');assert d.version=='0.5.0';p=pathlib.Path(d._path).resolve();p.relative_to(pathlib.Path("+repr(str(site))+").resolve());assert [(e.name,e.value) for e in d.entry_points if e.group=='pytest11']==[('instafail','pytest_instafail')];print(str(p))"
    meta=pathlib.Path(subprocess.check_output([sys.executable,'-c',code],cwd=work,env=env,text=True).strip())
    for p in meta.rglob('*'):
        if p.is_file():owned(p)
    # Unfiltered original tox command with no posargs; config and fixtures untouched.
    code="import runpy,sys;sys.argv=['pytest'];runpy.run_module('pytest',run_name='__main__')"
    subprocess.run([sys.executable,'-c',code],cwd=work,env=env,check=True)
    print(json.dumps({'route':'Original bare pytest command, setup.cfg --color=yes and original FORCE_COLOR=1','original_files':len(manifest),'runtime_files':1,'commands':[['pytest']],'runtime_origin':str(module),'engine':'installed-RPM' if installed else 'buildroot-wheel','boundary':'All seven original test methods and both three-way fixture parameter sets retained; no filters/new skip/xfail. Original Option sets n=None, so worker-labelled fixture cases are not claimed as xdist workers. Current Python3.11/distro pytest is tested separately from unclaimed legacy tox pytest5/6/interpreter/platform matrix.'}))
PY

%files
%license LICENSE
%doc README.rst CHANGES.rst
%{python3_sitelib}/pytest_instafail.py
%{python3_sitelib}/__pycache__/pytest_instafail*.pyc
%{python3_sitelib}/pytest_instafail-*.dist-info/
%{_datadir}/python-pytest-instafail/

%changelog
* Tue Oct 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.5.0-1
- Initial fixed release, all original bare pytest defaults and BSD-3 notice.
