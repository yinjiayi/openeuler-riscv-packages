# SPDX-License-Identifier: Apache-2.0
Name:           python-contextlib2
Version:        21.6.0
Release:        3%{?dist}
Summary:        Backports and enhancements for the contextlib module
License:        Python-2.0 AND Apache-2.0
URL:            https://github.com/jazzband/contextlib2
Source0:        python-contextlib2-21.6.0.tar.gz
Source1:        TYPESHED-LICENSE.txt
Patch0:         0001-python311-context-protocol-errors.patch
Patch1:         0002-context-manager-stub-signatures.patch
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-coverage
BuildRequires:  python3-mypy
BuildRequires:  python3-typing-extensions
Requires:       python3
Requires:       python3-coverage
Requires:       python3-mypy
Requires:       python3-typing-extensions

%description
Backports of standard-library context managers, asynchronous context managers,
and exit stacks. The complete original tests and type hints are retained.

%prep
%setup -q -n contextlib2-94174bafebe58a79af6059883f604624ab087d18
mkdir -p ../contextlib2-pristine
cp -a . ../contextlib2-pristine/
%patch -P 0 -p1
%patch -P 1 -p1

%build
# VERSION.txt is original21.6.0; no SCM substitution or backend patch.
SOURCE_DATE_EPOCH=315532800 %{__python3} -m pip wheel --no-deps --no-index --no-build-isolation --wheel-dir wheelhouse .

%install
%{__python3} -m pip install --no-deps --no-index --no-compile --root %{buildroot} --prefix %{_prefix} wheelhouse/contextlib2-21.6.0-*.whl
install -d %{buildroot}%{_datadir}/python-contextlib2/original
cp -a ../contextlib2-pristine/. %{buildroot}%{_datadir}/python-contextlib2/original/
install -d %{buildroot}%{_datadir}/python-contextlib2/compat
install -m 0644 test/test_contextlib.py %{buildroot}%{_datadir}/python-contextlib2/compat/test_contextlib.py
install -m 0644 %{PATCH0} %{buildroot}%{_datadir}/python-contextlib2/compat/0001-python311-context-protocol-errors.patch
install -m 0644 contextlib2/__init__.pyi %{buildroot}%{_datadir}/python-contextlib2/compat/contextlib2.pyi
install -m 0644 %{PATCH1} %{buildroot}%{_datadir}/python-contextlib2/compat/0002-context-manager-stub-signatures.patch
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/python-contextlib2/python-contextlib2-21.6.0.tar.gz
install -m 0644 %{SOURCE1} TYPESHED-LICENSE.txt
install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/python-contextlib2/TYPESHED-LICENSE.txt
cat > %{buildroot}%{_datadir}/python-contextlib2/original-files.json <<'JSON'
{".coveragerc": "b8d7dab81a8dbcb958c78848d0a4a2dee67b33aa76fbc6b10a135dd31a25c2dc", ".github/workflows/release.yml": "7951ae3094f9b8e9285e584a96a28f1c5723b94c8a82410ac37345aac7d732d6", ".github/workflows/test.yml": "bcb6bf35dbe810e571c1179b1b34028a5d312ec7d1858d22ccefdea1683656d9", ".gitignore": "1da36ebd4a01f1eb07befab5e6063ae0e6384af73da047c58d5ce29c851c2714", "CONTRIBUTING.md": "8d50e7e2bf9ab61c08a399717e0578c25fd7ffcd5b1ba33553788dacfb7048e9", "LICENSE.txt": "1d689012e239a17c182b3ccb355ce7682a61c937ebfe1ad57185c6e853ca2f25", "MANIFEST.in": "ee84a5ca46cce7757d955e7b0726e15e0d8ae9b5dcb921afc99e28dcf09a613e", "NEWS.rst": "27f50c51244a20912a0e1725290565d0d9f049ea15d609856b6aa978630b7791", "README.rst": "f374182a332571bb4ad03f283d4b38f747e4c77fb9d1bc5bc2fc27cd9e76b01c", "VERSION.txt": "6bf203f1cce6fe35a755b58b19c1fc6b922a384bc1520536de793e678c87784b", "contextlib2/__init__.py": "07133aada065936c0179de03f80b1a1e973d753803fc2f957cb37e9a527943d3", "contextlib2/__init__.pyi": "903d67317ec73ac673ba6ccb63ed0b86a74c2dc1ab5b2dc36734f1ce3362b6ac", "contextlib2/py.typed": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "dev/mypy.allowlist": "435fadd88d00db7d236e2f3cce683379e8c396fb636afde76781a55e6906aafc", "dev/py3_10_contextlib_pyi_to_contextlib2_pyi.patch": "c091e0324c2e2747d0825d2cf87cb915c0fb9cc491ebd28751164e5b2cc83bdb", "dev/py3_10_contextlib_rst_to_contextlib2_rst.patch": "745eadad26d662ac4419e241e5c39c97bef816c7fe6bf13333bc66ecba045264", "dev/py3_10_contextlib_to_contextlib2.patch": "02f91074f19ead52e944b799f036e1863362efa3cf31c85c90fc9bbd16aef469", "docs/Makefile": "5ef1a9b1426da48646d9a9c4f6f3ab0e2d84e431fd81dd3115bd15a5f10a1ef4", "docs/conf.py": "74bc47ecd46f72a54dbd1ea3fd8616b273748d20991649979ab915ee91435019", "docs/contextlib2.rst": "41f5a19ea3381f7af792a1e1d90da6c0feb2ed52aea9314e31e8debe9c182de1", "docs/index.rst": "db98feb4999a60675dedd74d72982d4c085e0246a7f16bf718c4131e29869ef5", "docs/make.bat": "101d136bbf866c71a0532c6c7a2c7ff30ef6cd430b8806e7d7d11e10ed1581fe", "setup.cfg": "78a84014cdc83d884f629d75d03c9c78c57b5159f3b4a9876573ff333d42b9a3", "setup.py": "439efd32aef174e2567334c152c8705a54f7cef3ea7bbe28ced8ff93704e293a", "test/__init__.py": "7dedc958ff5270dabbcfa95d294e932561ffaacb5c6ef4a68df921e6ae1860d4", "test/support/__init__.py": "e14f4f5792e5f3745d4829ffc101d068c4746f22db93e75916cdfc636f1935b5", "test/support/os_helper.py": "39d162cbbf9f683ba34a1bae2decd83dfa68c8127c42d8ca25a094b2a826940a", "test/test_contextlib.py": "93d7bc3c1a45eadd525fbeb36cfa2ae45090e6f71564dd6f31c2095e471fff99", "test/test_contextlib_async.py": "a42a88bafe7cdd64fb2a973fa31c5cb855c5469ebb269057e2081e5f0078246e", "tox.ini": "bbc7de7acaf3103034ba8d530884fd23548ae940d927a376fc1055c8e77e6927"}
JSON

%check
env -u PYTHONHOME -u PYTHONSTARTUP -u COVERAGE_PROCESS_START -u PYTEST_ADDOPTS -u PYTEST_PLUGINS -u PYTHONPATH %{__python3} - "%{buildroot}%{_datadir}/python-contextlib2/original" "%{buildroot}%{python3_sitelib}" buildroot <<'PY'
import hashlib,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text())
runtime={p.removeprefix('contextlib2/'):h for p,h in manifest.items() if p.startswith('contextlib2/')}
runtime['__init__.pyi']='56e610be65ede3f15ae9d6ba17bca4167a04a5092bacb76ef28cdef5a128d9a5'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%%{NAME}',str(p)],text=True)=='python-contextlib2'
assert len(manifest)==30 and set(runtime)=={'__init__.py','__init__.pyi','py.typed'}
for p,h in manifest.items():
    q=original/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
for p,h in runtime.items():
    q=site/'contextlib2'/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
archive=original.parent/'python-contextlib2-21.6.0.tar.gz';license_text=original.parent/'TYPESHED-LICENSE.txt'
assert digest(archive)=='4c541b6043ab276d80b906783573a2d2d190843957858a7ae7917f94d906538b' and digest(license_text)=='b41b78f562a2e65b75cab44354335f6f435d4ef73065509600ac910cf4e22fe0'
owned(archive);owned(license_text);owned(original.parent/'original-files.json')
compatible=original.parent/'compat'/'test_contextlib.py'
assert compatible.is_file() and not compatible.is_symlink() and digest(compatible)=='0b09b42b6666060b9657815309d4aac3ae3f7b60f4ee415149a0a9b78a80d760'
owned(compatible);owned(original.parent/'compat'/'0001-python311-context-protocol-errors.patch')
compatible_stub=original.parent/'compat'/'contextlib2.pyi'
assert compatible_stub.is_file() and not compatible_stub.is_symlink() and digest(compatible_stub)==runtime['__init__.pyi']
owned(compatible_stub)
for filename,expected_patch in [('0001-python311-context-protocol-errors.patch','ad006efcb1fbaba5b7416ad24af9ab26ac3047f8f3e525df18f707800517b97c'),('0002-context-manager-stub-signatures.patch','ed5365ef29249bc0d30d580260d2c81ae599305bd7faf624cc51066bc4b5f7f7')]:
    q=original.parent/'compat'/filename;assert q.is_file() and not q.is_symlink() and digest(q)==expected_patch;owned(q)
for base,expected in ((original,manifest),(site/'contextlib2',runtime)):
    for p in base.rglob('*'):
        if not p.is_file():continue
        rel=p.relative_to(base).as_posix()
        if rel in expected:continue
        assert p.parent.name=='__pycache__' and p.suffix=='.pyc' and any(p.name.startswith(pathlib.Path(x).stem+'.') and p.parent.parent==base/pathlib.Path(x).parent for x in expected if x.endswith('.py')),rel
        owned(p)
guard="""import hashlib,importlib.abc,importlib.machinery,importlib.metadata,json,os,pathlib,sys
site=pathlib.Path(SITE_JSON).resolve();expected=json.loads(RUNTIME_JSON)
def fail_closed():os._exit(86)
if any(n=='contextlib2' or n.startswith('contextlib2.') for n in sys.modules):fail_closed()
class OriginGuard(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname=='contextlib2' or fullname.startswith('contextlib2.'):
            try:
                spec=importlib.machinery.PathFinder.find_spec(fullname,path)
                if not spec or not spec.origin:fail_closed()
                p=pathlib.Path(spec.origin).resolve();rel=p.relative_to(site/'contextlib2').as_posix()
                if rel not in expected or hashlib.sha256(p.read_bytes()).hexdigest()!=expected[rel]:fail_closed()
                return spec
            except BaseException:fail_closed()
        return None
sys.meta_path.insert(0,OriginGuard())
# Verify guarded runtime first, then unload only candidate modules so original
# coverage discovery still measures their complete top-level code.
try:
    import contextlib2
    p=pathlib.Path(contextlib2.__file__).resolve()
    if p!=site/'contextlib2'/'__init__.py' or hashlib.sha256(p.read_bytes()).hexdigest()!=expected['__init__.py']:fail_closed()
    print(json.dumps({'guarded_runtime_origin':str(p),'sha256':expected['__init__.py']}),file=sys.stderr)
    for n in list(sys.modules):
        if n=='contextlib2' or n.startswith('contextlib2.'):del sys.modules[n]
except BaseException:fail_closed()
# Discovery imports all scratch test/support; only two declared exception
# assertions select the Python 3.11 protocol semantics in the compat test copy.
# The declared shipped-stub hash maps seven signatures to existing runtime
# methods; the complete pristine stub and original allowlist stay unchanged.
# It cannot import a source contextlib2 package because that copy is absent.
""".replace('SITE_JSON',repr(str(site))).replace('RUNTIME_JSON',repr(json.dumps(runtime)))
commands=[['coverage','run','-m','unittest','discover','-t','.','-s','test'],['coverage','report'],['coverage','xml'],['python','-m','mypy.stubtest','--allowlist','dev/mypy.allowlist','contextlib2']]
with tempfile.TemporaryDirectory(prefix='python-contextlib2-defaults-') as scratch:
    work=pathlib.Path(scratch)/'original';work.mkdir()
    for p in manifest:
        if p.startswith('contextlib2/'):continue
        dst=work/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/p,dst)
    shutil.copyfile(compatible,work/'test'/'test_contextlib.py')
    assert not (work/'contextlib2').exists()
    env=dict(os.environ)
    for key in ('PYTHONHOME','PYTHONSTARTUP','COVERAGE_PROCESS_START','PYTEST_ADDOPTS','PYTEST_PLUGINS'):env.pop(key,None)
    env.update(PYTHONPATH=str(site),PYTHONDONTWRITEBYTECODE='1')
    code=guard+'\nd=importlib.metadata.distribution("contextlib2");assert d.version=="21.6.0";p=pathlib.Path(d._path).resolve();p.relative_to(site);print(str(p))\n'
    metadata_path=pathlib.Path(subprocess.check_output([sys.executable,'-c',code],cwd=work,env=env,text=True).strip())
    for p in metadata_path.rglob('*'):
        if p.is_file():owned(p)
    for argv in commands:
        if argv[0]=='coverage':module='coverage';child_argv=argv
        else:module='mypy.stubtest';child_argv=['mypy.stubtest',*argv[3:]]
        code=guard+'\nimport runpy\nsys.argv='+repr(child_argv)+'\nrunpy.run_module('+repr(module)+',run_name="__main__")\n'
        subprocess.run([sys.executable,'-c',code],cwd=work,env=env,check=True)
    print(json.dumps({'route':'Complete original CPython tox coverage/unittest/stubtest commands on target Python3.11','original_files':len(manifest),'compatibility_test_sha256':digest(compatible),'compatibility_stub_sha256':digest(compatible_stub),'runtime_files':len(runtime),'commands':commands,'distribution':'contextlib2','runtime_origin':str(site/'contextlib2'),'engine':'installed-RPM' if installed else 'buildroot-wheel','boundary':'All30 pristine originals retained byte-identical. First declared test-only patch selects exact version-specific protocol errors in two tests; second stub-only patch declares five existing concrete exits and two actual coroutine signatures. Runtime implementation, all tests/support, coverage settings and two-entry mypy allowlist retained, no added filter, skip, xfail or waiver. Legacy interpreter matrix, CI orchestration and external Codecov/PyPI upload remain unclaimed.'}))
PY

%files
%license LICENSE.txt TYPESHED-LICENSE.txt
%doc README.rst NEWS.rst
%{python3_sitelib}/contextlib2/
%{python3_sitelib}/contextlib2-*.dist-info/
%{_datadir}/python-contextlib2/

%changelog
* Tue Oct 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 21.6.0-3
- Match seven shipped type-hint signatures to existing runtime methods.
- Preserve the full original stubtest and strict patched-stub origin hashes.
* Tue Oct 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 21.6.0-2
- Preserve all tests and select exact Python 3.11 context protocol exceptions.
* Mon Oct 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 21.6.0-1
- Initial fixed release, original full CPython default checks and complete licenses.
