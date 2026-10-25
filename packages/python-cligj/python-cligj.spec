# SPDX-License-Identifier: Apache-2.0
Name:           python-cligj
Version:        0.7.2
Release:        1%{?dist}
Summary:        Click arguments and options for GeoJSON command line interfaces
License:        BSD-3-Clause
URL:            https://github.com/mapbox/cligj
Source0:        python-cligj-0.7.2.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-coverage
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-cov
BuildRequires:  python3-click >= 4.0
Requires:       python3
Requires:       python3-coverage
Requires:       python3-pytest
Requires:       python3-pytest-cov
Requires:       python3-click >= 4.0

%description
Click arguments, options and feature parsers for the Python GeoJSON ecosystem.

%prep
%setup -q -n cligj-b837c2cdd8811dff04f95cdfd0234efe6c638eab
mkdir -p ../cligj-pristine
cp -a . ../cligj-pristine/

%build
SOURCE_DATE_EPOCH=315532800 %{__python3} -m pip wheel --no-deps --no-index --no-build-isolation --wheel-dir wheelhouse .

%install
%{__python3} -m pip install --no-deps --no-index --no-compile --root %{buildroot} --prefix %{_prefix} wheelhouse/cligj-0.7.2-*.whl
install -d %{buildroot}%{_datadir}/python-cligj/original
cp -a ../cligj-pristine/. %{buildroot}%{_datadir}/python-cligj/original/
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/python-cligj/python-cligj-0.7.2.tar.gz
cat > %{buildroot}%{_datadir}/python-cligj/original-files.json <<'JSON'
{".gitignore": "7ebafce83505424442272eabb6ecd110c1d7f0d28edaf2c9152252265e901092", ".travis.yml": "4e2cfe274af26e72fb796c093a4357e08e85eb739c7f566fb33b62e358e8600d", "CHANGES.txt": "25cb0be6743878ddb73ca9e2fb1ea3349d3bd99e8bd591b96f870a40f318e65c", "LICENSE": "5902d716544ddf9a34849b345c391abaf7c21ca16ed22706d6ac2f5503712594", "MANIFEST.in": "b5304150a4017d5015245aaa898a5de08b87a3988a88ce763e1675c597886396", "README.rst": "9f055c8d5112c009da55a888c67fe879bf64bd00b310c65d3b017a5d03233c4a", "cligj/__init__.py": "cef0fc29ce4f718f80a291ea18863e21e923bf9dc15214420fa147885d24f2e3", "cligj/features.py": "1705478f488076ab4e3b2d2e0859650ba1f411536ab1fdc38e3f7d544058a825", "setup.cfg": "cda75b9adb3accd6d0d994428abe8bc699d2d6d886bc9991203accf63ffe9f48", "setup.py": "395eaab4e2f8e4f29876411604ae730332ff6b4682bda655f2e299f598facb2a", "tests/conftest.py": "d09e30c161f2a7ef1b07ae1b11a922a89085486ee9b1d89b9252c3d746d01ddd", "tests/onepoint.geojson": "ed87ea915aa878c70defd1dec524f803b86de20a3954919a90c5bcf00da94ddd", "tests/point_pretty_geom.txt": "9b553c4e9b1a2795f9807e98eccaa705d4e68f878d0f996c75decc4cef19abb4", "tests/test_cli.py": "8cbcc2d67612b01c73ae924b4b2ae3b027c0a2ee7cc334e55eed317bc4af26f1", "tests/test_features.py": "41ee205d035442e85f70d0b2070c414474b04d3831701cc10faa9c1061d5e24c", "tests/twopoints-pretty.json": "74f97749aaf6f73f9ad3ca35bff6bab7404dbefa667ced9097b64ca9f4349f07", "tests/twopoints.geojson": "56729023295e60f89febd6b24f888024e5f61f1024bd60f4fde20914e47532d5", "tests/twopoints_geom_seq.txt": "c6f4442890732e6a5a59f55ed6ff483e1a6961d7d8bdb71d75990e82e7ab1941", "tests/twopoints_geom_seqrs.txt": "769edc344549c660db999b391b56cd01dfd74992c7fb3c654eeb16c2facbe6cb", "tests/twopoints_seq.txt": "1244e54790282799ed6bcded0258bbfe8bca0f042e3d6b3195235a49b542b22d", "tests/twopoints_seqrs.txt": "e4e09e446e94ac4257c43be192ca85ca3f2a8a9b805a78d4df4be2c0f763890c"}
JSON


%check
%{__python3} - "%{buildroot}%{_datadir}/python-cligj/original" "%{buildroot}%{python3_sitelib}" buildroot <<'PY'
import hashlib,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text())
runtime={p.removeprefix('cligj/'):h for p,h in manifest.items() if p.startswith('cligj/')}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%%{NAME}',str(p)],text=True)=='python-cligj'
assert len(manifest)==21 and len(runtime)==2
for p,h in manifest.items():
    q=original/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
for p,h in runtime.items():
    q=site/'cligj'/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
if installed:
    archive=original.parent/'python-cligj-0.7.2.tar.gz';assert digest(archive)=='dc340a1dcc13ba0215b7782e91bcaa45b6f36d573847ecc07ccc88c0cf8e3cd6';owned(archive);owned(original.parent/'original-files.json')
for base,expected in ((original,manifest),(site/'cligj',runtime)):
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
        if fullname=='cligj' or fullname.startswith('cligj.'):
            spec=importlib.machinery.PathFinder.find_spec(fullname,path);assert spec and spec.origin
            p=pathlib.Path(spec.origin).resolve();rel=p.relative_to(site/'cligj').as_posix()
            assert rel in expected and hashlib.sha256(p.read_bytes()).hexdigest()==expected[rel],(fullname,str(p))
            return spec
        return None
sys.meta_path.insert(0,OriginGuard())
# Do not preload runtime before original pytest-cov instrumentation.
""".replace('SITE_JSON',repr(str(site))).replace('RUNTIME_JSON',repr(json.dumps(runtime)))
with tempfile.TemporaryDirectory(prefix='python-cligj-defaults-') as scratch:
    work=pathlib.Path(scratch)/'original';work.mkdir()
    for p in manifest:
        if p.startswith('cligj/'):continue
        dst=work/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/p,dst)
    assert not (work/'cligj').exists()
    env=dict(os.environ,PYTHONPATH=str(site),PYTHONDONTWRITEBYTECODE='1')
    args=['--cov','cligj','--cov-report','term-missing']
    code=guard+'\nimport runpy\nsys.argv='+repr(['py.test']+args)+'\nrunpy.run_module("pytest",run_name="__main__")\n'
    subprocess.run([sys.executable,'-c',code],cwd=work,env=env,check=True)
    code=guard+'\nd=importlib.metadata.distribution("cligj");assert d.version=="0.7.2";p=pathlib.Path(d._path).resolve();p.relative_to(site);print(str(p))\n'
    metadata_path=pathlib.Path(subprocess.check_output([sys.executable,'-c',code],cwd=work,env=env,text=True).strip())
    for p in metadata_path.rglob('*'):
        if p.is_file():owned(p)
    print(json.dumps({'route':'Original shared Travis py.test coverage default on target Python3.11','original_files':len(manifest),'runtime_files':len(runtime),'commands':[['py.test']+args],'runtime_origin':str(site/'cligj'),'engine':'installed-RPM' if installed else 'buildroot-wheel','boundary':'Whole original tests/config/fixtures retained. Legacy interpreter matrix, external Coveralls upload and PyPI publication unclaimed.'}))
PY

%files
%license LICENSE
%doc README.rst CHANGES.txt
%{python3_sitelib}/cligj/
%{python3_sitelib}/cligj-*.dist-info/
%{_datadir}/python-cligj/

%changelog
* Mon Oct 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7.2-1
- Initial package preserving original shared pytest defaults and BSD notices.
