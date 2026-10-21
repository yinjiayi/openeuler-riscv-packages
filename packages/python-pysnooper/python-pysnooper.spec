# SPDX-License-Identifier: Apache-2.0
Name:           python-pysnooper
Version:        1.2.3
Release:        1%{?dist}
Summary:        Line and variable tracing debugger for Python
License:        MIT AND PSF-2.0
URL:            https://github.com/cool-RR/PySnooper
Source0:        python-pysnooper-1.2.3.tar.gz
Source1:        CONTEXTLIB2-LICENSE.txt
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-pytest
Requires:       python3
Requires:       python3-pytest

%description
Trace executed lines, local variables and exceptions using a decorator or
context manager. The original complete tests and vendored support are retained.

%prep
%setup -q -n PySnooper-0561a89c0ec88d11f38c6ef815d12c0423300fe1
mkdir -p ../pysnooper-pristine
cp -a . ../pysnooper-pristine/

%build
# Original explicit version and setuptools backend; no SCM or source patch.
SOURCE_DATE_EPOCH=315532800 %{__python3} -m pip wheel --no-deps --no-index --no-build-isolation --wheel-dir wheelhouse .

%install
%{__python3} -m pip install --no-deps --no-index --no-compile --root %{buildroot} --prefix %{_prefix} wheelhouse/*.whl
install -d %{buildroot}%{_datadir}/python-pysnooper/original
cp -a ../pysnooper-pristine/. %{buildroot}%{_datadir}/python-pysnooper/original/
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/python-pysnooper/python-pysnooper-1.2.3.tar.gz
install -m 0644 %{SOURCE1} CONTEXTLIB2-LICENSE.txt
install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/python-pysnooper/CONTEXTLIB2-LICENSE.txt
cat > %{buildroot}%{_datadir}/python-pysnooper/original-files.json <<'JSON'
{".gitignore": "0751d50628aa7e90bc54eedd39b5c508f2f3bcd7ef006c01e95336f8653df64f", ".travis.yml": "6e90eaf4cdd9bf7d90c502783a9ac23c6a28036c369b50331c7ae3b96abcb9e9", "ADVANCED_USAGE.md": "1df193aa9e9296dd1947edbeede7c9a878274c6b58995f24f09631635edde8fc", "AUTHORS": "dafdb28f1d45655c2f7df4683800f16d631445fa11e6ea7b5f8d459e0f8a03e6", "LICENSE": "5db83d6347f7e52946b736c71d0d59bb80c8a4485fcfa0a5140bdd839152be88", "MANIFEST.in": "2f56bab5e6994c60589587dfff5dedaff3d9fb2dff37e7e11d6376c9b4edd86e", "README.md": "5e813d7f69182f094e8b2d8ea731b2512cb2c5a2e7cbbc36866bd3bcee18e70c", "make_release.sh": "3cce292b1825471c2a821f6a37eda352d78e0671d99099c655d7a607c2396665", "misc/IDE files/PySnooper.wpr": "66fe28c766b5a4c1f4dd429a02e0701decb28a775c1e6ee75fe516b7d590aafb", "misc/generate_authors.py": "fbd94292a89a6247db4d9934e6b65c0a49f0f291c66ff7ea29c97c5d549643ef", "misc/output.jpg": "3d80895d090ff35598908f32c0926fc3f7ccb809185507f96e2ba77535f70a10", "pyproject.toml": "0d2df4e9048f74f759f835775a4bb1f586923dc5bdfb27781abdf0282fa882d9", "pysnooper/__init__.py": "0124c5831cfe86180a1f5be23c240de762681ac2575f785f335a885bc11e4d30", "pysnooper/pycompat.py": "e1051bf6207cd8868e9fba0c4dcf45ef87151a0b0009929e6b2909ae219e7b27", "pysnooper/tracer.py": "a2d1dd118022304ecf9daa42540ae5927d6864bede083625c6fb65c7a2d62d50", "pysnooper/utils.py": "da054266ab14393c2c7864de4373d3b81dab3d6c257d78da12f78e07978e05bc", "pysnooper/variables.py": "cb1f7476d0c6c0d32dc0576dfe24869a5b87c2f9152d6e43c3f0d8a0ffcb273d", "requirements.in": "1a22fd72190dc52814abfa96e60d359a0aa3cd1d8f85f55a8d6725cff85131cd", "requirements.txt": "44c91d4c293a45e5efd6e28c304835637cccbdb5de9b88136c03bcfb98376d8d", "setup.cfg": "6163ad6209ff0487d48288a440f97a3f16eb99913256756da2c64c9ac56e1d38", "setup.py": "9d94e62a5e6e1746a6185cfe5c4f5706923f81f3ded6ffebf526ea21df9fe2a5", "tests/__init__.py": "cf29ef59772b7309424b9229e607daca365cc178249a31f7b1c2ae748bfd1893", "tests/mini_toolbox/__init__.py": "ae283723ccc17351e07af95a3ab517dc2d3f9e060ae7c294e6c48048eab2852b", "tests/mini_toolbox/contextlib.py": "a71a862643c583543f81d18b5e546cadd7423f7796ed80533447d2280960f921", "tests/mini_toolbox/pathlib.py": "de455cfd2904f2f8a7de1af77c8c447557f89e1c8d7192b4442c9e119c4793fa", "tests/samples/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "tests/samples/exception.py": "08178aa61be130b580e4d8c4f8bf734978a117b15ad6bf4d2241951ba666090e", "tests/samples/indentation.py": "f53b7a0364eaf94c52844b4027f4d6e467181881aa45053b6c1f92d5f6e400f5", "tests/samples/recursion.py": "3d1c5adb351e3062d6ba14b212df800a1a1ab266a017f070b0a9d3b767233b17", "tests/test_chinese.py": "fba0c36e6e95c576a3ac46e8876716ed768ce252dd23dea8ef2f3cc2400e13cc", "tests/test_mini_toolbox.py": "7dd4dc0fde5198016f8e08867cabdd17019a97acceb7356408326ef632d6f210", "tests/test_multiple_files/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "tests/test_multiple_files/multiple_files/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "tests/test_multiple_files/multiple_files/bar.py": "a8ffcccbc13e6d39792e53f638c8b8b431ea807be46a7eae58cd4e5ee6c36534", "tests/test_multiple_files/multiple_files/foo.py": "e1386152b69de58453f1fcd186200694ad5e8b0bedba2e3af575b570184699f3", "tests/test_multiple_files/test_multiple_files.py": "089a7a8cea73086bea472ec7938f689d04c533b245fd927b9e6af925bc532169", "tests/test_not_implemented.py": "27a07cc7444c543eac1987244780504588e44011871c0ba59f679f1d51921cd7", "tests/test_pysnooper.py": "fbf059355bf937ab199f1014edafcd300dcf392a6b61d5043d5560bbee9acbc7", "tests/test_utils/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "tests/test_utils/test_ensure_tuple.py": "a0d511d6b0817fd41a99cc7d76c85befac20a4ee65fc2526f5388a292ad00d77", "tests/test_utils/test_regex.py": "fd9f5dab4cf1d87300db4919373757cadf2df9177e6a440aa65bce6019729d73", "tests/utils.py": "02bb3a647f89b8c38b5d678347486ccbbe3821ba9f0c108390408e88d26cdc01", "tox.ini": "7fc9664194133505c945a83ffda73ff6155aef3a4430d82276679de0bf350986"}
JSON

%check
env -u PYTHONHOME -u PYTHONSTARTUP -u COVERAGE_PROCESS_START -u PYTEST_ADDOPTS -u PYTEST_PLUGINS -u PYTHONPATH -u PYSNOOPER_DISABLED %{__python3} - "%{buildroot}%{_datadir}/python-pysnooper/original" "%{buildroot}%{python3_sitelib}" buildroot <<'PY'
import hashlib,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text())
runtime={p.removeprefix('pysnooper/'):h for p,h in manifest.items() if p.startswith('pysnooper/')}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%%{NAME}',str(p)],text=True)=='python-pysnooper'
assert len(manifest)==43 and set(runtime)=={'__init__.py','pycompat.py','tracer.py','utils.py','variables.py'}
for p,h in manifest.items():
    q=original/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
for p,h in runtime.items():
    q=site/'pysnooper'/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
archive=original.parent/'python-pysnooper-1.2.3.tar.gz';license_text=original.parent/'CONTEXTLIB2-LICENSE.txt'
assert digest(archive)=='01380deec408700ce91ebc9880991a31f0d8a171dd12a14012d7fb302df71fbc' and digest(license_text)=='c6a7affac6acdad2d2dd87d2d768438624ab692618db1f02bea3b11d3f3978f0'
owned(archive);owned(license_text);owned(original.parent/'original-files.json')
for base,expected in ((original,manifest),(site/'pysnooper',runtime)):
    for p in base.rglob('*'):
        if not p.is_file():continue
        rel=p.relative_to(base).as_posix()
        if rel in expected:continue
        assert p.parent.name=='__pycache__' and p.suffix=='.pyc' and any(p.name.startswith(pathlib.Path(x).stem+'.') and p.parent.parent==base/pathlib.Path(x).parent for x in expected if x.endswith('.py')),rel
        owned(p)
guard="""import hashlib,importlib.abc,importlib.machinery,importlib.metadata,json,os,pathlib,sys
site=pathlib.Path(SITE_JSON).resolve();expected=json.loads(RUNTIME_JSON)
def fail_closed():os._exit(86)
if any(n=='pysnooper' or n.startswith('pysnooper.') for n in sys.modules):fail_closed()
class OriginGuard(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname=='pysnooper' or fullname.startswith('pysnooper.'):
            try:
                spec=importlib.machinery.PathFinder.find_spec(fullname,path)
                if not spec or not spec.origin:fail_closed()
                p=pathlib.Path(spec.origin).resolve();rel=p.relative_to(site/'pysnooper').as_posix()
                if rel not in expected or hashlib.sha256(p.read_bytes()).hexdigest()!=expected[rel]:fail_closed()
                return spec
            except BaseException:fail_closed()
        return None
sys.meta_path.insert(0,OriginGuard())
try:
    import pysnooper
    p=pathlib.Path(pysnooper.__file__).resolve()
    if p!=site/'pysnooper'/'__init__.py' or hashlib.sha256(p.read_bytes()).hexdigest()!=expected['__init__.py']:fail_closed()
    print(json.dumps({'guarded_runtime_origin':str(p),'sha256':expected['__init__.py']}),file=sys.stderr)
except BaseException:fail_closed()
""".replace('SITE_JSON',repr(str(site))).replace('RUNTIME_JSON',repr(json.dumps(runtime)))
commands=[['pytest']]
with tempfile.TemporaryDirectory(prefix='python-pysnooper-defaults-') as scratch:
    work=pathlib.Path(scratch)/'original';work.mkdir()
    for p in manifest:
        if p.startswith('pysnooper/'):continue
        dst=work/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/p,dst)
    assert not (work/'pysnooper').exists()
    env=dict(os.environ)
    for key in ('PYTHONHOME','PYTHONSTARTUP','COVERAGE_PROCESS_START','PYTEST_ADDOPTS','PYTEST_PLUGINS','PYSNOOPER_DISABLED'):env.pop(key,None)
    env.update(PYTHONPATH=str(site),PYTHONDONTWRITEBYTECODE='1')
    code=guard+'\nd=importlib.metadata.distribution("PySnooper");assert d.version=="1.2.3";p=pathlib.Path(d._path).resolve();p.relative_to(site);print(str(p))\n'
    metadata_path=pathlib.Path(subprocess.check_output([sys.executable,'-c',code],cwd=work,env=env,text=True).strip())
    for p in metadata_path.rglob('*'):
        if p.is_file():owned(p)
    for argv in commands:
        code=guard+'\nimport runpy\nsys.argv='+repr(argv)+'\nrunpy.run_module("pytest",run_name="__main__")\n'
        subprocess.run([sys.executable,'-c',code],cwd=work,env=env,check=True)
    print(json.dumps({'route':'Original shared tox pytest {posargs} with no posargs on target Python3.11','original_files':len(manifest),'runtime_files':len(runtime),'commands':commands,'distribution':'PySnooper','runtime_origin':str(site/'pysnooper'),'engine':'installed-RPM' if installed else 'buildroot-wheel','boundary':'All original test/config/vendor/support bytes and original strict-markers/default timing tolerance retained. No filters/new skip/xfail or performance claim. Legacy interpreter/lint/security/readme/requirements/publish jobs remain unclaimed.'}))
PY

%files
%license LICENSE CONTEXTLIB2-LICENSE.txt tests/mini_toolbox/pathlib.py
%doc README.md AUTHORS
%{python3_sitelib}/pysnooper/
%{python3_sitelib}/[Pp]y[Ss]nooper-*.dist-info/
%{_datadir}/python-pysnooper/

%changelog
* Tue Oct 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.3-1
- Initial fixed release, original full pytest defaults and precise MIT/PSF notices.
