# SPDX-License-Identifier: Apache-2.0
Name:           python-click-default-group
Version:        1.2.4
Release:        1%{?dist}
Summary:        Default subcommands for Click groups
License:        BSD-3-Clause
URL:            https://github.com/click-contrib/click-default-group
Source0:        python-click-default-group-1.2.4.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-flit-core >= 3.2
BuildRequires:  python3-flit-core < 4
BuildRequires:  python3-wheel
BuildRequires:  python3-pytest
BuildRequires:  python3-click
Requires:       python3
Requires:       python3-click
Requires:       python3-pytest

%description
Extend Click groups with a default command while retaining all original tests.

%prep
%setup -q -n click-default-group-429c066978162c2cfabb14ea287aa6131413c324
mkdir -p ../click-default-group-pristine
cp -a . ../click-default-group-pristine/

%build
SOURCE_DATE_EPOCH=315532800 %{__python3} -m pip wheel --no-deps --no-index --no-build-isolation --wheel-dir wheelhouse .

%install
%{__python3} -m pip install --no-deps --no-index --no-compile --root %{buildroot} --prefix %{_prefix} wheelhouse/*.whl
install -d %{buildroot}%{_datadir}/python-click-default-group/original
cp -a ../click-default-group-pristine/. %{buildroot}%{_datadir}/python-click-default-group/original/
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/python-click-default-group/python-click-default-group-1.2.4.tar.gz
cat > %{buildroot}%{_datadir}/python-click-default-group/original-files.json <<'JSON'
{".github/workflows/test.yaml": "14583e56341ff51805b526543d99751202bb1ce0c377ddbf1bf95e67bc9dda8f", ".gitignore": "e4360df8ef9a539f076c291a7df08698315778fa391d20d57be8fef80986f0cb", ".travis.yml": "724640f4fa795958260b51e38e0c7b84d60557120f13be3ab0fb92123b8f5234", "LICENSE": "ec684181160e02c9e25c09dbfb32cc8278bb6bb3e84d7d9570a059ca55e4c118", "README.md": "ccb0f7819324c5e521df6976a400b37b111d9a3052872b9d5a6eb16706728342", "click_default_group.py": "ba904089bee5665af516d5be3021e1767effdae08dc75dd197470267d0b2a11d", "pyproject.toml": "468d9120b435135dce9439d0f226dd65a2b61a807f6b5d9036963e5ce8711180", "setup.cfg": "3da628bf6880dfb83d281c93f373f9a44f4907ffea96716d18aebe3e90cd4d55", "test.py": "a87f17e3d549d2719530a594227de1da3e31f070b45d2e09282106e35c08a351"}
JSON

%check
env -u PYTHONHOME -u PYTHONSTARTUP -u COVERAGE_PROCESS_START -u PYTEST_ADDOPTS -u PYTEST_PLUGINS -u PYTHONPATH %{__python3} - "%{buildroot}%{_datadir}/python-click-default-group/original" "%{buildroot}%{python3_sitelib}" buildroot <<'PY'
import hashlib,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text());runtime_hash=manifest['click_default_group.py']
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%%{NAME}',str(p)],text=True)=='python-click-default-group'
assert len(manifest)==9
for p,h in manifest.items():
    q=original/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
module=site/'click_default_group.py';assert module.is_file() and not module.is_symlink() and digest(module)==runtime_hash;owned(module)
archive=original.parent/'python-click-default-group-1.2.4.tar.gz'
assert digest(archive)=='7cc73659fa479e1a41e6a133c0233bf7162c212b34b84381a1a09e366b9c065c';owned(archive);owned(original.parent/'original-files.json')
for p in original.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(original).as_posix()
    if rel in manifest:continue
    assert p.parent.name=='__pycache__' and p.suffix=='.pyc' and any(p.name.startswith(pathlib.Path(x).stem+'.') and p.parent.parent==original/pathlib.Path(x).parent for x in manifest if x.endswith('.py')),rel
    owned(p)
guard="""import hashlib,importlib.abc,importlib.machinery,importlib.metadata,json,os,pathlib,sys
site=pathlib.Path(SITE_JSON).resolve();expected=HASH_JSON
def fail_closed():os._exit(86)
if any(n=='click_default_group' or n.startswith('click_default_group.') for n in sys.modules):fail_closed()
class OriginGuard(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname=='click_default_group' or fullname.startswith('click_default_group.'):
            try:
                spec=importlib.machinery.PathFinder.find_spec(fullname,path)
                if not spec or not spec.origin:fail_closed()
                p=pathlib.Path(spec.origin).resolve()
                if p!=site/'click_default_group.py' or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:fail_closed()
                return spec
            except BaseException:fail_closed()
        return None
sys.meta_path.insert(0,OriginGuard())
try:
    import click_default_group
    p=pathlib.Path(click_default_group.__file__).resolve()
    if p!=site/'click_default_group.py' or hashlib.sha256(p.read_bytes()).hexdigest()!=expected or click_default_group.__version__!='1.2.4':fail_closed()
    print(json.dumps({'guarded_runtime_origin':str(p),'sha256':expected}),file=sys.stderr)
except BaseException:fail_closed()
""".replace('SITE_JSON',repr(str(site))).replace('HASH_JSON',repr(runtime_hash))
commands=[['pytest']]
with tempfile.TemporaryDirectory(prefix='python-click-default-group-defaults-') as scratch:
    work=pathlib.Path(scratch)/'original';work.mkdir()
    for p in manifest:
        if p=='click_default_group.py':continue
        dst=work/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/p,dst)
    assert not (work/'click_default_group.py').exists()
    env=dict(os.environ)
    for key in ('PYTHONHOME','PYTHONSTARTUP','COVERAGE_PROCESS_START','PYTEST_ADDOPTS','PYTEST_PLUGINS'):env.pop(key,None)
    env.update(PYTHONPATH=str(site),PYTHONDONTWRITEBYTECODE='1')
    code=guard+'\nd=importlib.metadata.distribution("click-default-group");assert d.version=="1.2.4";p=pathlib.Path(d._path).resolve();p.relative_to(site);print(str(p))\n'
    metadata_path=pathlib.Path(subprocess.check_output([sys.executable,'-c',code],cwd=work,env=env,text=True).strip())
    for p in metadata_path.rglob('*'):
        if p.is_file():owned(p)
    for argv in commands:
        code=guard+'\nimport runpy\nsys.argv='+repr(argv)+'\nrunpy.run_module("pytest",run_name="__main__")\n'
        subprocess.run([sys.executable,'-c',code],cwd=work,env=env,check=True)
    print(json.dumps({'route':'Original current GitHub Actions shared bare pytest on target CPython3.11/official distro Click8.1.7','original_files':len(manifest),'commands':commands,'runtime_origin':str(module),'engine':'installed-RPM' if installed else 'buildroot-wheel','boundary':'All7 original test functions/config/assertions preserved; no filters/new skip/pin relaxation. Original Click8.1.6 and older matrix environments and legacy Travis orchestration/reporting not reproduced.'}))
PY

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/click_default_group.py
%{python3_sitelib}/__pycache__/click_default_group*.pyc
%{python3_sitelib}/click_default_group-*.dist-info/
%{_datadir}/python-click-default-group/

%changelog
* Tue Oct 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.4-1
- Fixed official source, intact original defaults and RPM-owned runtime checks.
