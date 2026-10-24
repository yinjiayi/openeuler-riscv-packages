# SPDX-License-Identifier: Apache-2.0
Name:           python-makefun
Version:        1.16.0
Release:        1%{?dist}
Summary:        Create Python functions with explicit signatures
License:        BSD-3-Clause AND CC-BY-SA-4.0
URL:            https://github.com/smarie/python-makefun
Source0:        python-makefun-1.16.0.tar.gz
Source1:        CC-BY-SA-4.0.txt
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip > 19
BuildRequires:  python3-setuptools >= 39.2
BuildRequires:  python3-setuptools < 72
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-wheel
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-asyncio
Requires:       python3
Requires:       python3-pytest
Requires:       python3-pytest-asyncio

%description
Generate Python functions while preserving explicit signatures and defaults.

%prep
%setup -q -n python-makefun-197b14827c1b7830c0288477c007e1f1592f52ad
mkdir -p ../makefun-pristine
cp -a . ../makefun-pristine/
cp -p %{SOURCE1} CC-BY-SA-4.0.txt
cat > MAKEFUN-ATTRIBUTION.txt <<'NOTICE'
Makefun derivative-test attribution and change notice

The adapted excerpt in tests/test_so.py::test_so_decorator is distributed
under Creative Commons Attribution-ShareAlike 4.0 International.
This scope is the adapted test excerpt, not the makefun runtime library.

Title: How to make a chain of function decorators?
Source: https://stackoverflow.com/questions/739654/how-to-make-a-chain-of-function-decorators/1594484#1594484
Author: Bite code (formerly e-satis); subsequent contributors are credited in
the original public revision history:
https://stackoverflow.com/posts/1594484/revisions
Original revision: 993bdbaa-429a-47e5-adda-755d2adc582e,
posted 2009-10-20 13:05. The original makebold/makeitalic example is reused
with makefun.wraps, the hello function/name, assertions and help checks added
by the upstream Makefun authors. These are adaptations, not an endorsement.
Related example by Paolo Bergantino, posted 2009:
https://stackoverflow.com/questions/739654/how-to-make-a-chain-of-function-decorators/739665#739665

The pre-2011 original contribution is CC BY-SA 2.5:
https://stackoverflow.com/help/licensing
https://creativecommons.org/licenses/by-sa/2.5/legalcode.en
Its section4(b) permits the same license elements in a later version;
the adapted excerpt is distributed under CC BY-SA 4.0:
https://creativecommons.org/licenses/by-sa/4.0/legalcode.txt
The full4.0 license text is installed beside this notice. No warranty or
endorsement is implied; no additional restrictions are imposed on the excerpt.
The separate library remains under its original full BSD3 LICENSE with all
Sylvain Marie/Schneider Electric notices, and the original PEP380 public-domain
attribution/change note is preserved. Packaging helpers are Apache-2.0.
All41 upstream files remain byte-for-byte unchanged. This notice is not a
claim that all Stack Overflow examples are exclusively BSD-licensed.
NOTICE

%build
SETUPTOOLS_SCM_PRETEND_VERSION=1.16.0 SOURCE_DATE_EPOCH=315532800 %{__python3} -m pip wheel --no-deps --no-index --no-build-isolation --wheel-dir wheelhouse .

%install
%{__python3} -m pip install --no-deps --no-index --no-compile --root %{buildroot} --prefix %{_prefix} wheelhouse/makefun-1.16.0-py2.py3-none-any.whl
install -d %{buildroot}%{_datadir}/python-makefun/original
cp -a ../makefun-pristine/. %{buildroot}%{_datadir}/python-makefun/original/
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/python-makefun/python-makefun-1.16.0.tar.gz
install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/python-makefun/CC-BY-SA-4.0.txt
install -m 0644 MAKEFUN-ATTRIBUTION.txt %{buildroot}%{_datadir}/python-makefun/MAKEFUN-ATTRIBUTION.txt
cat > %{buildroot}%{_datadir}/python-makefun/original-files.json <<'JSON'
{".github/workflows/base.yml": "11677a5e4f577fb76f07f1eaaccfd6202e0d87af5a6694ce3af3bfe63c6dabf3", ".github/workflows/ghpages.yml": "08e00339b1de67267c684b38b3efab68102c614a3c4d3109cb3a552719d091fb", ".github/workflows/updater.yml": "b1e69f068debfc396d8975b8abb9285efc08a38920b31a6e36c97d36b1946fb1", ".gitignore": "5a14a0245d475f05581fe18e55c54d016881984fbfcb00d8fa134747ea286783", "LICENSE": "00eea85b9eafb7acd6c3b7c34a12b25a67c9c7d421838ced8ff3aca1823d1273", "README.md": "165fc0672b7759a5bcf308d52c3c6be2c154a96e185b458ae7b85c0adb72315c", "ci_tools/.pylintrc": "2a9d216dc0dec082014ca38409d5e7ae704bd634fd493d4f1cd3311edd2eb926", "ci_tools/check_python_version.py": "9acabf67073f2c7c5ef96779b4c8386c094158668446dc805272c0fd12c3977c", "ci_tools/flake8-requirements.txt": "805ef44984f033c557bed25377954fced2910aa10d6c683c6b0311fe73c3b912", "ci_tools/github_release.py": "ec5f27b71d9c8d0f7a7629deb18ee0602d333718d11f13971ed7dcc53f26c3bb", "ci_tools/nox_utils.py": "4d7d2fa7edd1bde329891a33a5a7bb2e288f8f2830702215019deb6154d1a55f", "docs/api_reference.md": "03cf568dc4561ca63514d3c36a0aa745bf269c5ca7db941315c8a161b253eee5", "docs/changelog.md": "3deef066f792e43d35a66069ffd13448345b11842ad4f9082a05273b794e4986", "docs/index.md": "11455b20fc7316325b797ed484e3ee8fa107ca1f0d656c22f1ccf9c769fb561a", "docs/long_description.md": "39b8d0be8b652c304424e1a222e6e23b63dbfb0ea2ef2c81c0cd7f869020d3ab", "mkdocs.yml": "114cba70faf1cfd72f821f5f92c8ccbdcd36d214d448fec014504649bd147e4e", "noxfile-requirements.txt": "bb8edaccc6e44dff57419f06119913513465ef92ff73c11032ae32309bbb8fb3", "noxfile.py": "fe5ec141ce91f45b59533665f9e382aa946f19f71e41912022be35e23bc8c3b5", "pyproject.toml": "e979b4cc8613ea6eabb829a798da2a7e73eb84868f61f546793141acf344bd04", "setup.cfg": "3afbcb5c05e8e1628dc81dac7be410b0896f87c645d23ebf875c07b3c1b53adc", "setup.py": "1dd1c9296f56f6f85f8f1089343bb093db89e00b51630e14255c8d8a8c4149aa", "src/makefun/__init__.py": "6dd4e94da73e00638b46befe7acbb61ba41a119ceb3a8908ca9ef7d3e56f201b", "src/makefun/_main_legacy_py.py": "c2d1810f1885b3d61ec46f2c6f91ed55f4ac97f74eed46def2c4f762315ae107", "src/makefun/_main_py35_and_higher.py": "a471776b3fc1f3e2aeb221174a1de30ae48166b9faec73a608545185e101fd50", "src/makefun/_main_py36_and_higher.py": "d7ad87d05c5ec5c663cb01900a69d2aa15c052076ae69859379db52466b1fe44", "src/makefun/main.py": "5ef7645116febda9bc4731ac8337f4b3c4e5c16705f8218359173001e509567c", "src/makefun/py.typed": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "tests/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "tests/_issue_85_module.py": "13997ba9c7adac86e363864b987ca48c9f01813c23b925a23acf854af6baaf2f", "tests/_test_py35.py": "110d1493bd8d44830d2a85190de8abb4cdca4f1b6d3d3fced2bd0c296124a840", "tests/_test_py36.py": "5c4561222d16ff0e14368e54e88cc8241d11e01b19ac2923f1b8b588ac0a5d1d", "tests/_test_py38.py": "5859b81a48ae779e341dcfa62646d6b15d265e754814910ae954a098fc020905", "tests/test_advanced.py": "91400cd347d1b8260d0d5d344773fa4443e95a663346114d8bd5958a9a3ad4e4", "tests/test_compile_deco.py": "379b23ffce53c654fce7835432a1281b6ad80bee14e130a50c5277955ebd4e69", "tests/test_create_from_signature.py": "f564df9fbefc5b058f4feae5ba41e59716cf84c8232fe6bde8b99ad0f6d37899", "tests/test_create_from_string.py": "3daaedacc7fe9dc709a1acca897198edd435c23fd7d5c4feaf99fb439501d5a4", "tests/test_doc.py": "4e8119307d5e400e9a244c8af7d8035e542dce585245db254628e2f40128b654", "tests/test_generators_coroutines.py": "381970050fcf0273ad6dec9b4b054a4a0d0152ed10f16a6547ebbe1dc1ff8a0e", "tests/test_issues.py": "4deba869cc3afad4cd178be440830197524485680fcfd9b3d4bf03418c4ebedb", "tests/test_partial_and_macros.py": "d2363ccc6427025e25f29d734c1f46fcf0dff7820f31ad357d4e77d8e47f1e0f", "tests/test_so.py": "f85f88edfd90c738d9423d716cfad0ae50ff5a4023dc72db3cc11e5b705aa35f"}
JSON

%check
env -u PYTHONHOME -u PYTHONSTARTUP -u COVERAGE_PROCESS_START -u PYTEST_ADDOPTS -u PYTEST_PLUGINS -u PYTHONPATH %{__python3} - "%{buildroot}%{_datadir}/python-makefun/original" "%{buildroot}%{python3_sitelib}" buildroot <<'PY'
import ast,hashlib,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text());runtime={p.removeprefix('src/'):h for p,h in manifest.items() if p.startswith('src/makefun/')}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%%{NAME}',str(p)],text=True)=='python-makefun'
assert len(manifest)==41 and len(runtime)==6
for p,h in manifest.items():
    q=original/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
for p,h in runtime.items():
    q=site/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
versionfile=site/'makefun/_version.py';assert versionfile.is_file() and not versionfile.is_symlink();owned(versionfile)
tree=ast.parse(versionfile.read_text());assert len(tree.body)==2
values={}
for node in tree.body:
    assert isinstance(node,ast.Assign) and len(node.targets)==2 and all(isinstance(x,ast.Name) for x in node.targets)
    for target in node.targets:values[target.id]=ast.literal_eval(node.value)
assert values=={'__version__':'1.16.0','version':'1.16.0','__version_tuple__':(1,16,0),'version_tuple':(1,16,0)}
assert tree.body[0].targets[0].id=='__version__' and tree.body[1].targets[0].id=='__version_tuple__'
runtime['makefun/_version.py']=digest(versionfile)
for p in (site/'makefun').rglob('*'):
    if not p.is_file():continue
    assert not p.is_symlink();rel=p.relative_to(site).as_posix()
    if rel not in runtime:assert p.parent.name=='__pycache__' and p.suffix=='.pyc' and any(p.name.startswith(pathlib.Path(x).stem+'.') and p.parent.parent==site/pathlib.Path(x).parent for x in runtime if x.endswith('.py')),rel
    owned(p)
archive=original.parent/'python-makefun-1.16.0.tar.gz';assert digest(archive)=='e632cd8cea81ec69ca17718896da11fb60ae472fbab186438b6703f9b176edd5';owned(archive);owned(original.parent/'original-files.json')
for name,expected in [('CC-BY-SA-4.0.txt','28a9529c7d0bb4dc51f4bf5c116a3d16ef247a052f7591466768ddf563fd1cf5'),('MAKEFUN-ATTRIBUTION.txt','1707b762021e149cc91ae26bd4d99f43b9fbf0b1102524238f881fa7fcc0f128')]:
    p=original.parent/name;assert p.is_file() and not p.is_symlink() and digest(p)==expected;owned(p)
guard="""import hashlib,importlib.abc,importlib.machinery,importlib.metadata,json,os,pathlib,sys
site=pathlib.Path(SITE_JSON).resolve();expected=HASH_JSON
def fail_closed():os._exit(86)
if sys.version_info[:2]!=(3,11) or any(n=='makefun' or n.startswith('makefun.') for n in sys.modules):fail_closed()
try:
    if importlib.metadata.version('pytest')!='7.4.4' or importlib.metadata.version('pytest-asyncio')!='0.21.1':fail_closed()
except BaseException:fail_closed()
class OriginGuard(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname=='makefun' or fullname.startswith('makefun.'):
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
    import makefun
    p=pathlib.Path(makefun.__file__).resolve()
    if p!=site/'makefun/__init__.py' or makefun.__version__!='1.16.0':fail_closed()
    print(json.dumps({'guarded_runtime_origin':str(p),'runtime_sha256':expected,'python':list(sys.version_info[:3]),'pytest':importlib.metadata.version('pytest'),'pytest_asyncio':importlib.metadata.version('pytest-asyncio')}),file=sys.stderr)
except BaseException:fail_closed()
""".replace('SITE_JSON',repr(str(site))).replace('HASH_JSON',repr(runtime))
with tempfile.TemporaryDirectory(prefix='python-makefun-defaults-') as scratch:
    work=pathlib.Path(scratch)/'original';work.mkdir()
    for p in manifest:
        if p.startswith('src/makefun/'):continue
        dst=work/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/p,dst)
    assert not (work/'src/makefun').exists()
    env=dict(os.environ)
    for key in ('PYTHONHOME','PYTHONSTARTUP','COVERAGE_PROCESS_START','PYTEST_ADDOPTS','PYTEST_PLUGINS'):env.pop(key,None)
    env.update(PYTHONPATH=str(site),PYTHONDONTWRITEBYTECODE='1',PYTHONNOUSERSITE='1')
    code=guard+'\nd=importlib.metadata.distribution("makefun");assert d.version=="1.16.0";p=pathlib.Path(d._path).resolve();p.relative_to(site);print(str(p))\n'
    metadata=pathlib.Path(subprocess.check_output([sys.executable,'-c',code],cwd=work,env=env,text=True).strip())
    for p in metadata.rglob('*'):
        if p.is_file():owned(p)
    # Original CPython3.11 nox tests session, coverage=False: unchanged argv/config.
    code=guard+'\nimport runpy\nsys.argv=["pytest","--cache-clear","-v","tests/"]\nrunpy.run_module("pytest",run_name="__main__")\n'
    subprocess.run([sys.executable,'-c',code],cwd=work,env=env,check=True)
    # Additional behavioral replay, not four extra pytest passes: unchanged bodies.
    replay=[('tests.test_generators_coroutines','test_native_coroutine'),('tests.test_generators_coroutines','test_issue_96'),('tests.test_issues','test_issue_77_async_generator_wraps'),('tests.test_issues','test_issue_77_async_generator_partial')]
    code=guard+'\nimport asyncio,importlib,inspect\nreplay='+repr(replay)+'\n'
    code+='for module,name in replay:\n m=importlib.import_module(module);p=pathlib.Path(m.__file__).resolve();rel=p.relative_to(pathlib.Path.cwd()).as_posix();assert rel in ORIGINAL_HASHES and hashlib.sha256(p.read_bytes()).hexdigest()==ORIGINAL_HASHES[rel];f=getattr(m,name);assert inspect.iscoroutinefunction(f) and len(inspect.signature(f).parameters)==0;asyncio.run(f());print(json.dumps({"supplementary_awaited_original":module+"::"+name,"source_sha256":ORIGINAL_HASHES[rel]}))\n'
    code=code.replace('ORIGINAL_HASHES',repr(manifest))
    subprocess.run([sys.executable,'-c',code],cwd=work,env=env,check=True)
    for p,h in manifest.items():assert digest(original/p)==h
    for p,h in runtime.items():assert digest(site/p)==h
    print(json.dumps({'route':'Original CPython3.11 python -m pytest --cache-clear -v tests/; supplementary four original awaited bodies','original_files':41,'runtime_files':7,'original_commands':[['python','-m','pytest','--cache-clear','-v','tests/']],'supplementary_awaited_bodies':replay,'generated_runtime_sha256':runtime['makefun/_version.py'],'engine':'installed-RPM' if installed else 'buildroot-wheel','boundary':'Original cfg doctest/ignore_glob/warnings and skips preserved. Strict-plugin four skips must be reported as skips; separate awaited assertions are not pytest passes. Other nox sessions/matrix, coverage70/report, docs/lint/build/publish unclaimed.'}))
PY

%files
%license LICENSE CC-BY-SA-4.0.txt MAKEFUN-ATTRIBUTION.txt
%doc README.md
%{python3_sitelib}/makefun/
%{python3_sitelib}/makefun-*.dist-info/
%{_datadir}/python-makefun/

%changelog
* Wed Oct 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.16.0-1
- Fixed original sources and preserved CPython3.11 defaults with installed origin guards.
