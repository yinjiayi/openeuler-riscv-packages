# SPDX-License-Identifier: Apache-2.0
Name:           python-iterable-io
Version:        1.0.4
Release:        1%{?dist}
Summary:        Adapt generators and other iterables to a file-like interface
License:        LGPL-3.0-only
URL:            https://github.com/pR0Ps/iterable-io
Source0:        python-iterable-io-1.0.4.tar.gz
Source1:        LGPL-3.0-only.txt
Source2:        GPL-3.0-only.txt
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-hatchling
BuildRequires:  python3-build
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-cov
BuildRequires:  python3-coverage
Requires:       python3
Requires:       python3-pytest
Requires:       python3-pytest-cov
Requires:       python3-coverage

%description
Iterable-io adapts generators and other iterables to a file-like interface.

%prep
%setup -q -n iterable-io-9cdce76c27930cc1db80b360a9c22b7dc3b35828
mkdir -p ../iterable-io-pristine
cp -a . ../iterable-io-pristine/
# Supplemental versioned SPDX terms; upstream source/config remain pristine.
cp %{SOURCE1} LGPL-3.0-only.txt
cp %{SOURCE2} GPL-3.0-only.txt

%build
SOURCE_DATE_EPOCH=315532800 %{__python3} -m build . --wheel --no-isolation

%install
%{__python3} -m pip install --no-deps --no-index --no-compile --root %{buildroot} --prefix %{_prefix} dist/iterable_io-1.0.4-*.whl
install -d %{buildroot}%{_datadir}/python-iterable-io/original
cp -a ../iterable-io-pristine/. %{buildroot}%{_datadir}/python-iterable-io/original/
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/python-iterable-io/python-iterable-io-1.0.4.tar.gz
cat > %{buildroot}%{_datadir}/python-iterable-io/original-files.json <<'JSON'
{".github/workflows/tests.yml":"4b3a1f3f8b66c6fbdd8642384bfd59fa8547a3351b58f53ff6d68d919011d9d9",".gitignore":"d27c48704f37ff3c41a8ce0a6063687c0935abddd8a9bc6610499570666aee03","CHANGELOG.md":"b12454e563962f48c8029ca76727cb2320f3694f9d4ec08454530e6903d2204c","README.md":"c4f4abfe995a0cae92ba76ac346493b6ca76f86fb406ba8b65038c71f37886e1","pyproject.toml":"6b0535f84aaf2832a93be85ec302afff6bf721eaa04e5c19c64ddd99c0ab16a0","src/iterableio/__init__.py":"8b2fbc6103ca9ee407a52fd5c1b8ab0d3a659ed91ebee69e61ff4bfb9120644f","tests/test_iteratorio.py":"60b3334391493283e6bd896ac11e0132dfab5273bd5a063682739fdc0618da23"}
JSON

%check
%{__python3} -I - "%{buildroot}%{_datadir}/python-iterable-io/original" "%{buildroot}%{python3_sitelib}" buildroot <<'PY'
# SPDX-License-Identifier: Apache-2.0
"""Remote-only intact original defaults against the selected buildroot/RPM wheel."""
import hashlib,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile,xml.etree.ElementTree as ET
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text())
assert len(manifest)==7
runtime={'__init__.py':manifest['src/iterableio/__init__.py']}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%%{NAME}',str(p)],text=True)=='python-iterable-io'
for name,h in manifest.items():
    p=original/name;assert p.is_file() and not p.is_symlink() and digest(p)==h;owned(p)
for rel,h in runtime.items():
    p=site/'iterableio'/rel;assert p.is_file() and not p.is_symlink() and digest(p)==h;owned(p)
archive=original.parent/'python-iterable-io-1.0.4.tar.gz'
assert digest(archive)=='63275efd51c0af44f1c4a5f070eb9642a33e17d16fe052dc06a377411bcd39a5';owned(archive);owned(original.parent/'original-files.json')
for p in original.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(original).as_posix()
    if rel in manifest:continue
    assert p.parent.name=='__pycache__' and p.suffix=='.pyc' and any(p.name.startswith(pathlib.Path(x).stem+'.') and p.parent.parent==original/pathlib.Path(x).parent for x in manifest if x.endswith('.py')),rel
    owned(p)
guard="""import hashlib,importlib.abc,importlib.machinery,os,pathlib,sys,traceback
site=pathlib.Path(SITE_JSON).resolve();expected=RUNTIME_JSON
def fail_closed():
    traceback.print_exc();os._exit(88)
def checked(p):
    try:
        q=pathlib.Path(p)
        if q.is_symlink():raise AssertionError('candidate runtime symlink')
        q=q.resolve();rel=q.relative_to(site/'iterableio').as_posix()
        if rel not in expected or hashlib.sha256(q.read_bytes()).hexdigest()!=expected[rel]:raise AssertionError('candidate path/hash outside manifest')
    except BaseException:fail_closed()
if any(n=='iterableio' or n.startswith('iterableio.') for n in sys.modules):os._exit(88)
for rel in expected:checked(site/'iterableio'/rel)
class OriginGuard(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname=='iterableio' or fullname.startswith('iterableio.'):
            try:
                spec=importlib.machinery.PathFinder.find_spec(fullname,path)
                if not spec or not spec.origin:raise AssertionError('unmanifested candidate module')
                checked(spec.origin)
            except BaseException:fail_closed()
        return None
sys.meta_path.insert(0,OriginGuard())
def audit(event,args):
    if event=='exec':
        filename=args[0].co_filename
        if '/iterableio/' in filename.replace(chr(92),'/'):checked(filename)
sys.addaudithook(audit)
""".replace('SITE_JSON',repr(str(site))).replace('RUNTIME_JSON',repr(runtime))
with tempfile.TemporaryDirectory(prefix='python-iterable-io-defaults-') as scratch:
    scratch=pathlib.Path(scratch);work=scratch/'original';work.mkdir();guarddir=scratch/'guard';guarddir.mkdir();(guarddir/'sitecustomize.py').write_text(guard)
    for p in manifest:
        if p.startswith('src/iterableio/'):continue
        dest=work/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/p,dest)
    assert not (work/'src/iterableio').exists() and not (work/'iterableio').exists()
    env=dict(os.environ)
    for key in ('PYTHONHOME','PYTHONSTARTUP','COVERAGE_PROCESS_START','PYTEST_ADDOPTS','PYTEST_PLUGINS','PYTHONPATH'):env.pop(key,None)
    env.update(PYTHONPATH=os.pathsep.join([str(guarddir),str(site)]),PYTHONDONTWRITEBYTECODE='1')
    # Separate preflight process cannot preload library statements before pytest-cov starts.
    code="import importlib.metadata,json,pathlib,iterableio;d=importlib.metadata.distribution('iterable-io');print(json.dumps({'version':d.version,'dist':str(pathlib.Path(d._path).resolve()),'runtime':str(pathlib.Path(iterableio.__file__).resolve())}))"
    proof=json.loads(subprocess.check_output([sys.executable,'-c',code],cwd=work,env=env,text=True))
    assert proof['version']=='1.0.4' and proof['runtime']==str(site/'iterableio/__init__.py')
    metadata=pathlib.Path(proof['dist']);metadata.relative_to(site)
    for p in metadata.rglob('*'):
        if p.is_file():owned(p)
    print(json.dumps({'preflight':proof,'runtime_hashes':runtime,'original_files':len(manifest),'coverage_preload':False}),flush=True)
    report=scratch/'original-tests.xml'
    code="import runpy,sys;sys.argv=['py.test','--cov=iterableio','--junitxml='+sys.argv[1]];runpy.run_module('pytest',run_name='__main__')"
    subprocess.run([sys.executable,'-c',code,str(report)],cwd=work,env=env,check=True)
    suites=list(ET.parse(report).getroot().iter('testsuite'));assert suites
    totals={k:sum(int(s.attrib.get(k,0)) for s in suites) for k in ('tests','failures','errors','skipped')}
    assert totals=={'tests':20,'failures':0,'errors':0,'skipped':0},totals
    for rel,h in runtime.items():assert digest(site/'iterableio'/rel)==h
    for p,h in manifest.items():assert digest(original/p)==h
    print(json.dumps({'route':'Original unfiltered py.test --cov=iterableio against wheel','engine':'installed-RPM' if installed else 'buildroot-wheel','original_files':7,'runtime_files':1,'junit':totals,'commands':[['py.test','--cov=iterableio']],'reporting_only_added':'--junitxml isolated result, no filters/skip/threshold','boundary':'Original wheel build and Python3.11 default coverage route retained. Separate interpreter/OS matrix unclaimed; no added coverage threshold or timing/native proof.'}),flush=True)
PY

%files
%license LGPL-3.0-only.txt GPL-3.0-only.txt
%doc README.md CHANGELOG.md
%{python3_sitelib}/iterableio/
%{python3_sitelib}/iterable_io-*.dist-info/
%{_datadir}/python-iterable-io/

%changelog
* Tue Oct 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.4-1
- Preserve all original wheel-installed default tests and supplemental license terms.
