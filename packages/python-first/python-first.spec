# SPDX-License-Identifier: Apache-2.0
Name:           python-first
Version:        2.0.2
Release:        1%{?dist}
Summary:        Return the first true value of an iterable
License:        MIT
URL:            https://github.com/hynek/first
Source0:        python-first-2.0.2.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-pytest
BuildRequires:  make
Requires:       python3
Requires:       python3-pytest
Requires:       make

%description
First returns the first true value of an iterable, with optional default and key.

%prep
%setup -q -n first-294964dd2b7a68930ff520a58cdb314e58ecb1e7
mkdir -p ../first-pristine
cp -a . ../first-pristine/

%build
SOURCE_DATE_EPOCH=315532800 %{__python3} -m pip wheel --no-deps --no-index --no-build-isolation --wheel-dir wheelhouse .

%install
%{__python3} -m pip install --no-deps --no-index --no-compile --root %{buildroot} --prefix %{_prefix} wheelhouse/first-2.0.2-*.whl
install -d %{buildroot}%{_datadir}/python-first/original
cp -a ../first-pristine/. %{buildroot}%{_datadir}/python-first/original/
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/python-first/python-first-2.0.2.tar.gz
cat > %{buildroot}%{_datadir}/python-first/original-files.json <<'JSON'
{".gitignore": "bd23d2283b8a4840d2c055cbfd8ac65f03ce3a7e8c373e86209fd92346e469ab", ".travis.yml": "98cc9807d1f73462b2fa299b8a1124bff8946f77cf35cf9ffbdcc642313994ce", "AUTHORS.rst": "0e434f815d57e5925554ac5eb2d386ab2f9fe7a4cf2ba6d35972e399bcd9fef2", "CONTRIBUTING.rst": "1561626ee55be7954514a2bb5106fc17511c15e0e513f3f8715653106d036dc6", "HISTORY.rst": "abe2cc1a25155cfb2b522e1b26d8e2410d6d96187a737aea7bbcf05f8d751f65", "LICENSE": "db4f023d9e71791480d1ea447361fd87263ecaac5d420be3b5bb36c72e07c5c5", "MANIFEST.in": "82ddd0e96975bb694d6a92b8a6bc7cde2d7829d2018495be5b37a33c16044ff6", "Makefile": "7f79ca6e5008dc05e0b3a4d23a0ed8bde6fa915d96f84eb2e7d1c4d2dcc8e501", "README.rst": "87364fe21b432bd8608d30a9932e5ef12c15967a40e57a6b1d21374c86d88f55", "first.py": "274b865f244be606b1b99364c1ca3003e69e7cf1cd3cc09cbab7853ff455394a", "setup.cfg": "278ee0f897af2d7e04ad1e8023df61aab0bb08fd1c7c209d90c075c12bc337f1", "setup.py": "12f653a01bf767dbca996ff04a4f1bca00e9012804d43e4fd1bda2cc6054b43b", "test_first.py": "6f2d5108cdadce96b5e9603d28c37e3c8def319a248bbdb640b4ee6560d9d41a", "tox.ini": "65b21aa2b59d8c2d6a3dc1b6d87e4b50c41966c322e25a12616fa7d8385eb099"}
JSON

%check
%{__python3} - "%{buildroot}%{_datadir}/python-first/original" "%{buildroot}%{python3_sitelib}" buildroot <<'PY'
import hashlib,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%%{NAME}',str(p)],text=True)=='python-first'
assert len(manifest)==14
for p,h in manifest.items():
    q=original/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
runtime=site/'first.py';assert runtime.is_file() and not runtime.is_symlink() and digest(runtime)==manifest['first.py'];owned(runtime)
archive=original.parent/'python-first-2.0.2.tar.gz'
assert digest(archive)=='3bef6f02707b0789003109d2bf10fe78e309510f8ccdced0f54e3a40d2787dbc';owned(archive);owned(original.parent/'original-files.json')
for p in original.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(original).as_posix()
    if rel in manifest:continue
    assert p.parent.name=='__pycache__' and p.suffix=='.pyc' and any(p.name.startswith(pathlib.Path(x).stem+'.') and p.parent.parent==original/pathlib.Path(x).parent for x in manifest if x.endswith('.py')),rel
    owned(p)
dist=[d for d in importlib.metadata.distributions(path=[str(site)]) if d.metadata['Name']=='first']
assert len(dist)==1 and dist[0].version=='2.0.2'
metadata=pathlib.Path(dist[0]._path).resolve();metadata.relative_to(site)
for p in metadata.rglob('*'):
    if p.is_file():owned(p)
guard="""import hashlib,importlib.abc,importlib.util,os,pathlib,sys,traceback
try:
    runtime=pathlib.Path(RUNTIME_PATH).resolve()
    assert sys.version_info[:2]==(3,11)
    assert hashlib.sha256(runtime.read_bytes()).hexdigest()==RUNTIME_SHA
    class InstalledFirstGuard(importlib.abc.MetaPathFinder):
        def find_spec(self,fullname,path=None,target=None):
            if fullname=='first':return importlib.util.spec_from_file_location(fullname,str(runtime))
            return None
    sys.meta_path.insert(0,InstalledFirstGuard())
    import first
    assert pathlib.Path(first.__file__).resolve()==runtime
    assert hashlib.sha256(pathlib.Path(first.__file__).read_bytes()).hexdigest()==RUNTIME_SHA
    print('FIRST_DEFAULT_ORIGIN='+str(runtime),flush=True)
except BaseException:
    traceback.print_exc();os._exit(88)
""".replace('RUNTIME_PATH',repr(str(runtime))).replace('RUNTIME_SHA',repr(manifest['first.py']))
with tempfile.TemporaryDirectory(prefix='python-first-defaults-') as scratch:
    root=pathlib.Path(scratch);work=root/'original';work.mkdir();shim=root/'bin';shim.mkdir();hook=root/'guard';hook.mkdir()
    for p in manifest:
        if p=='first.py':continue
        dst=work/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/p,dst)
    # A symlink retains pytest's first.py module-doctest discovery but executes
    # only the installed, hash-verified module. The pristine original is intact.
    (work/'first.py').symlink_to(runtime)
    assert (work/'first.py').is_symlink() and os.path.samefile(work/'first.py',runtime)
    assert digest(work/'first.py')==manifest['first.py']
    (shim/'python').symlink_to(pathlib.Path(sys.executable).resolve())
    (hook/'sitecustomize.py').write_text(guard)
    env=dict(os.environ,PYTHONPATH=str(hook)+os.pathsep+str(site),PYTHONDONTWRITEBYTECODE='1',PYTHONNOUSERSITE='1',PATH=str(shim)+os.pathsep+'/usr/bin:/bin')
    for k in ('PYTEST_ADDOPTS','PYTEST_PLUGINS'):env.pop(k,None)
    # Exact original Travis entry point and unmodified Makefile command.
    subprocess.run(['make','test'],cwd=work,env=env,check=True)
    assert os.path.samefile(work/'first.py',runtime)
    for p,h in manifest.items():assert digest(original/p)==h and digest(work/p)==h
    assert digest(runtime)==manifest['first.py']
    print(json.dumps({'route':'Original shared Travis make test on target Python3.11','original_files':14,'command':['make','test'],'original_make_argv':['python','-m','pytest','--doctest-glob=*.rst','--doctest-modules','--ignore=setup.py'],'runtime_origin':str(runtime),'engine':'installed-RPM' if installed else 'buildroot-wheel','boundary':'All original module and RST doctests/unit tests retained. Separate make cov, legacy interpreter matrix, tox manifest and external PyPI-description routes retained but unclaimed.'}))
PY

%files
%license LICENSE
%doc README.rst HISTORY.rst AUTHORS.rst
%{python3_sitelib}/first.py
%{python3_sitelib}/__pycache__/first.*.pyc
%{python3_sitelib}/first-*.dist-info/
%{_datadir}/python-first/

%changelog
* Mon Oct 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.2-1
- Initial package preserving all original shared tests and module/RST doctests.
