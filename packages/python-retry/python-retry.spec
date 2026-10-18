# SPDX-License-Identifier: Apache-2.0
Name:           python-retry
Version:        0.9.5
Release:        1%{?dist}
Summary:        Easy to use retry decorator and retry-call helper
License:        Apache-2.0
URL:            https://github.com/eSAMTrade/retry
Source0:        python-retry-0.9.5.tar.gz
Source1:        LICENSE-2.0.txt
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-pbr
BuildRequires:  python3-pytest
BuildRequires:  python3-tox
BuildRequires:  python3-decorator >= 3.4.2
Requires:       python3
Requires:       python3-pbr
Requires:       python3-pytest
Requires:       python3-tox
Requires:       python3-wheel
Requires:       python3-decorator >= 3.4.2

%description
Retry decorators and retry-call helpers from the maintained eSAMTrade fork.
The upstream distribution is retry2 and its import package is retry; this
package does not coinstall the distinct invl retry distribution.

%prep
%setup -q -n retry-ff6e88999818070a3012191c3e949fbdc8131cae
mkdir -p ../retry-pristine
cp -a . ../retry-pristine/

%build
# PBR needs an explicit version for an immutable Git archive without .git.
# This equals the unmodified upstream setup.cfg release version and fixed tag.
PBR_VERSION=%{version} SOURCE_DATE_EPOCH=315532800 %{__python3} -m pip wheel --no-deps --no-index --no-build-isolation --wheel-dir wheelhouse .

%install
%{__python3} -m pip install --no-deps --no-index --no-compile --root %{buildroot} --prefix %{_prefix} wheelhouse/retry2-0.9.5-*.whl
install -d %{buildroot}%{_datadir}/python-retry/original
cp -a ../retry-pristine/. %{buildroot}%{_datadir}/python-retry/original/
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/python-retry/python-retry-0.9.5.tar.gz
install -m 0644 %{SOURCE1} LICENSE-2.0.txt
install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/python-retry/LICENSE-2.0.txt
cat > %{buildroot}%{_datadir}/python-retry/original-files.json <<'JSON'
{".gitignore": "63784cf4376ceb4100545f763f894e7a4901b6baf61d10e932a576f7287756e4", "AUTHORS": "341446e4f201d86f17b237c7ca20c62308afab32dc96b53e11ca6efc7acd10c1", "ChangeLog": "9e0128daf3852f0f3d40e80ef87e24e3cd430d6afd5d59cd864420073d838b86", "LICENSE": "f1a572d775bce1079a1764abfbf856756736790bad7fa4214eb72b9d44423b2b", "README.rst": "e0f3bae26883c912ee5b124ee6cd60c7fec6de7bfe79eed357d8f4cc8c8b543f", "requirements.txt": "4066a74d5c641bc6da212a4d99b545c8db6e5eaebe81131f6391eab6b1a6d8fc", "retry/__init__.py": "d2b685465ab0fe9bf217585076fd7da44dc3e0b07c093dd986aed0063f7358d7", "retry/api.py": "4d162e15218b91d494af2a1c5ee4aaf3d3fa131e07aa168629258ca8625a21e8", "retry/compat.py": "90fed86cc42d116d52eba2837fca05a81d598e588b18ad9a692171e12b2d9a96", "setup.cfg": "848d96b6cda0dbdd51d7088f0e94d97cbf27e120eb66e0f550cbd345649d600f", "setup.py": "acacf6aa76c6361a29948092554f82cdf45916382fca6de2edd64842a8052f8a", "test-requirements.txt": "7eba9fc077bc679c6263568fa6491caa916c06135bd4242c8f649e84d59b61d8", "tests/test_retry.py": "d33a406a109859e14c889377e20637b3eb0b359e52e5fdf154ac13eaf5ebf84d", "tox.ini": "db0f6b383f63a4678042249c13657447a0895a0e1147c1e8d27515a419927a4e", "upload.bat": "df405afb45028f330275dd288563ee7f6a6f80818c4fd546b2f6be2f0de5d311", "upload.sh": "d4213c94c471a898cb66c7653039008481122d8321e4a78674d4606ba492292f"}
JSON

%check
%{__python3} - "%{buildroot}%{_datadir}/python-retry/original" "%{buildroot}%{python3_sitelib}" buildroot <<'PY'
import hashlib,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text())
runtime={p.removeprefix('retry/'):h for p,h in manifest.items() if p.startswith('retry/')}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%%{NAME}',str(p)],text=True)=='python-retry'
assert len(manifest)==16 and len(runtime)==3
for p,h in manifest.items():
    q=original/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
for p,h in runtime.items():
    q=site/'retry'/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
archive=original.parent/'python-retry-0.9.5.tar.gz';license_text=original.parent/'LICENSE-2.0.txt'
assert digest(archive)=='e95a469cd75ad2ce3b0d7bb706e8c7f3e74c1681c7087d66af91c83a872ffd0c' and digest(license_text)=='cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30'
owned(archive);owned(license_text);owned(original.parent/'original-files.json')
for base,expected in ((original,manifest),(site/'retry',runtime)):
    for p in base.rglob('*'):
        if not p.is_file():continue
        rel=p.relative_to(base).as_posix()
        if rel in expected:continue
        assert p.parent.name=='__pycache__' and p.suffix=='.pyc' and any(p.name.startswith(pathlib.Path(x).stem+'.') and p.parent.parent==base/pathlib.Path(x).parent for x in expected if x.endswith('.py')),rel
        owned(p)
guard="""import hashlib,importlib.abc,importlib.machinery,importlib.metadata,json,pathlib,sys
site=pathlib.Path(SITE_JSON).resolve();expected=json.loads(RUNTIME_JSON)
class OriginGuard(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname=='retry' or fullname.startswith('retry.'):
            spec=importlib.machinery.PathFinder.find_spec(fullname,path);assert spec and spec.origin
            p=pathlib.Path(spec.origin).resolve();rel=p.relative_to(site/'retry').as_posix()
            assert rel in expected and hashlib.sha256(p.read_bytes()).hexdigest()==expected[rel],(fullname,str(p))
            return spec
        return None
sys.meta_path.insert(0,OriginGuard())
# No preload or source fallback; original pytest discovers the original tests.
""".replace('SITE_JSON',repr(str(site))).replace('RUNTIME_JSON',repr(json.dumps(runtime)))
with tempfile.TemporaryDirectory(prefix='python-retry-defaults-') as scratch:
    work=pathlib.Path(scratch)/'original';work.mkdir()
    for p in manifest:
        if p.startswith('retry/'):continue
        dst=work/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/p,dst)
    assert not (work/'retry').exists()
    env=dict(os.environ,PYTHONPATH=str(site),PYTHONDONTWRITEBYTECODE='1')
    code=guard+'\nimport runpy\nsys.argv=["py.test"]\nrunpy.run_module("pytest",run_name="__main__")\n'
    subprocess.run([sys.executable,'-c',code],cwd=work,env=env,check=True)
    code=guard+'\nd=importlib.metadata.distribution("retry2");assert d.version=="0.9.5";p=pathlib.Path(d._path).resolve();p.relative_to(site);print(str(p))\n'
    metadata_path=pathlib.Path(subprocess.check_output([sys.executable,'-c',code],cwd=work,env=env,text=True).strip())
    for p in metadata_path.rglob('*'):
        if p.is_file():owned(p)
    print(json.dumps({'route':'Original shared tox unfiltered py.test defaults on target Python3.11','original_files':len(manifest),'runtime_files':len(runtime),'commands':[['py.test']],'distribution':'retry2','runtime_origin':str(site/'retry'),'engine':'installed-RPM' if installed else 'buildroot-wheel','boundary':'All original tests/config/requirements retained; no selected checks removed. Legacy interpreter matrix, separate flake8 Python3.4 job and external upload scripts are unclaimed.'}))
PY

%files
%license LICENSE AUTHORS LICENSE-2.0.txt
%doc README.rst ChangeLog
%{python3_sitelib}/retry/
%{python3_sitelib}/retry2-*.dist-info/
%{_datadir}/python-retry/

%changelog
* Mon Oct 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.5-1
- Initial current eSAM Retry2 package, full Apache text and original pytest defaults.
