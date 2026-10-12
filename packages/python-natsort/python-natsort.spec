# SPDX-License-Identifier: Apache-2.0
Name:           python-natsort
Version:        8.4.0
Release:        1%{?dist}
Summary:        Simple flexible natural sorting for Python
License:        MIT
URL:            https://github.com/SethMMorton/natsort
Source0:        python-natsort-8.4.0.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-coverage
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-cov
BuildRequires:  python3-pytest-mock
BuildRequires:  python3-hypothesis
BuildRequires:  glibc-all-langpacks
Requires:       python3
Requires:       python3-coverage
Requires:       python3-pytest
Requires:       python3-pytest-cov
Requires:       python3-pytest-mock
Requires:       python3-hypothesis
Requires:       glibc-all-langpacks

%description
Natural sorting of strings and numbers, with original Unicode and locale handling.

%prep
%setup -q -n natsort-d9503c08f8f83ce8a89bfcc45fec136868756243
mkdir -p ../natsort-pristine
cp -a . ../natsort-pristine/

%build
SOURCE_DATE_EPOCH=315532800 %{__python3} -m pip wheel --no-deps --no-index --no-build-isolation --wheel-dir wheelhouse .

%install
%{__python3} -m pip install --no-deps --no-index --no-compile --root %{buildroot} --prefix %{_prefix} wheelhouse/natsort-8.4.0-*.whl
install -d %{buildroot}%{_datadir}/python-natsort/original
cp -a ../natsort-pristine/. %{buildroot}%{_datadir}/python-natsort/original/
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/python-natsort/python-natsort-8.4.0.tar.gz
cat > %{buildroot}%{_datadir}/python-natsort/original-files.json <<'JSON'
{".coveragerc": "c97423c7b3cc83fd1b45a49c55237f9be2d484896f27d388c01d2258405e45cb", ".github/ISSUE_TEMPLATE/bug_report.md": "c8f4f5a5ab2f40f457ed39229bbef4b9858d9220edbadebee96889b8a5e36bc6", ".github/ISSUE_TEMPLATE/feature_request.md": "1187e75fc070b41a2c00ea53478cf1497b5944397565e2b6dfe0c183fe56b89d", ".github/ISSUE_TEMPLATE/question.md": "883bba1ceeb64abd49f302433863c5a56cd2ab96314d25de919f3d26b10719b1", ".github/workflows/code-quality.yml": "98cf6c0539ce705622f0644f8fd494e721564da5e56beac3fb3724bfd294a874", ".github/workflows/deploy.yml": "8e52cd5dbd82dd565f53b7e3eab850dd0ee46e98d47a844c36e933fbb9619b76", ".github/workflows/tests.yml": "52341e0976a54f3dd28aa64c8299bdd28fc42c9e4bef66b9052b52aa5c4fb387", ".gitignore": "83c8da47dd789a81661cfe7b08340c34e3beb77c0f068f279c60df2a9f59cc47", "CHANGELOG.md": "f097bda9807ee09e2915206bbcdd0919b89fa2acd0b50b536402b2775843aa27", "CODE_OF_CONDUCT.md": "5173163cd48233274687df62dc5f5b07ebbfaa35928438f8b9ed90d1c7aa7124", "CONTRIBUTING.md": "16b9c529f81ad3267cd484d9a88e77ab360d7fee12b27f58e088a94593ef9772", "LICENSE": "81d078140eae25b31f257407190f4cdcb80177979749726e2aae4f2cdd90f623", "MANIFEST.in": "e2c6a85cee0b238189916220133a8573b9866489813790d016f5939440ffab53", "README.rst": "d2c09fb54346052e703fab4d26f182049bdd76dff97224d38fd5f45a06b4cffe", "RELEASING.md": "ddd8a230955c16f4d6805bce2e67e08a51463624d94504b15bab91fe46a8abb9", "dev/README.md": "1bbc983f27cb288cc049315b6f4e9ad127da661ccd9c8f2886f77162ca6e7f78", "dev/bump.py": "07364b9a1b4577ab66608621563664e59a8acb486dbf7c337f9cac2b29819d54", "dev/clean.py": "b65b9e9e1d933302b23fc65909070ea191aafa43e59791faf00d6bec63cb4d9e", "dev/generate_new_unicode_numbers.py": "daa6be40a15c52a7e179f492c698aaa03ddc74a083be69782778779222e39be9", "docs/api.rst": "8374fbd6310e10010f0f4bbe3a3a189cb6c5f854bf7eeff7f9e24dd48f933235", "docs/changelog.rst": "853e4a23cdf67121e0ff28bc40b952b94a871d45f394fcf40eb0ce2a73d8bc7c", "docs/conf.py": "cfa696e997a5315f00d027b8ab7067652a685a0138c4adb6f2d17584b98543a5", "docs/examples.rst": "9a949e238abbe877c2493b1ff9aff4da74ac5f35330b6897600ef840ce5cb9df", "docs/howitworks.rst": "5ba5f4421f2f7702e8c01e9a932d5b6228a2561ebef2715c542782630632b05c", "docs/index.rst": "8bd48e6760d1a4952fefeca13ee85c5ffc4cf3e5b283a7102321d02f369e4838", "docs/locale_issues.rst": "f3db32a2bae489faa56d3d6d83945d968d917abd43b528c3207a457d68fb4db8", "docs/shell.rst": "5d53d37cb898ae28d284897629ed0df4352f1c4af37058c911f39bf8df242654", "mypy_stubs/icu.pyi": "91525cd96ff9771bee319529f48d31521624221c6ab501b9097a4b50d38320fd", "natsort/__init__.py": "7f048962f662a51dbdaa4b1a73d20fb9f8a4f754a1348c5aec9ea4d910623041", "natsort/__main__.py": "fcbeb493980f2785b6bdbb57978b19d3f6170e2c6c884dd4301f48e25568f0b7", "natsort/compat/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "natsort/compat/fake_fastnumbers.py": "b19ebdb903dc29141fed59dddeb1bc390af9305c89e084a3e99b994f2234ae48", "natsort/compat/fastnumbers.py": "6590f70366d520b58a1c294e60b853250eba429c95498d803b675f0748dab253", "natsort/compat/locale.py": "595879d521af67b47cf570e58f956cfaf6b94fbf2a5462ab87d2d45264c925f8", "natsort/natsort.py": "a44112339530d3b42afc48ea938944581d300869875352440fc0dfaa1da00d7f", "natsort/ns_enum.py": "110a51c2b7a8bee25a0d4862a789eb999244b5cb5dd22c8f19aa1dde764d8f49", "natsort/py.typed": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "natsort/unicode_numbers.py": "ac1c969cdc55d186e6ba479483ae62d7800d8dc1d05d1cc677456b709dd5f433", "natsort/unicode_numeric_hex.py": "71265fd660f396c1d18ca3040f5cc2d375f17bb31611732d08f36712a99a228c", "natsort/utils.py": "64e2ac81a33c6a407e7a318b6d9fa04380dcf17a6f7e4cd44163a5c5e4f1cbed", "setup.cfg": "f4b310ff5a7c9da7b37c350a659f9af40d1018790144fb3904f083582ddc0d45", "setup.py": "14dc39ace6806a26e4bb4ca5e06dee45726625adcbe09bf80195c7df3174eba4", "tests/conftest.py": "cd8608c7c8aeb91e7f1e601f18d5bd5c5873828a1aba02561c1d260c68a85e39", "tests/profile_natsorted.py": "69c0dd3283ec2aee12d29bc4f34b9b94db2a117be1be424b98557d6ab11957a5", "tests/test_fake_fastnumbers.py": "f5550e9911219e6b7ad6bf192f6febd5e30a4bdf1afbc6b22e5124095fbdf8fa", "tests/test_final_data_transform_factory.py": "1d35cbcedd8206c8e6d7e5e168a6931664f838db0afafad135f46b7f5e63fe30", "tests/test_input_string_transform_factory.py": "ecafb0b483f6ba0090256009a9e094fa1bede88db1d2cfc8fb8bfb86d1fadb11", "tests/test_main.py": "ab5a5eef92d365fd8c866721f2cdbd7b266eca9486b603d0cc0fc7fef72fc98d", "tests/test_natsort_key.py": "d996ae8f7b8cdde8b680494771aa7bc3ebad3e2d58cc4922c5ef60ecda593e2d", "tests/test_natsort_keygen.py": "80ae4e9f520e2f96fa6902f79219fb6c17c30bf92e1b5c2af5ed8def221ece7f", "tests/test_natsorted.py": "cac223738f2717dc82f9dfcf14b926df77e51ce20b60207ea77306dccb77f531", "tests/test_natsorted_convenience.py": "b053d662f12e0ee900f6434e41bbc0b845a8bcf9d4ccd401d072b99b1f342d45", "tests/test_ns_enum.py": "f2d9f2900aaec98ce5d207bbcf28b941054670394a6ba0a63a4c1e9553e84fbb", "tests/test_os_sorted.py": "eff64c0770d31ca8df88ee59e00eaa9d14b29d1c170dd0ed34551df00f89aa1a", "tests/test_parse_bytes_function.py": "bfb96b27afea72968caaa24d793bad885ff8cb58f8caa65c138ad4df5865dd3d", "tests/test_parse_number_function.py": "7abadb6c366151ce838ea4736db2f0818d43c934adcc65623855f10992cfe5a1", "tests/test_parse_string_function.py": "001a3d82410da2fb284fe671022559ffb6af6a3f37da815cf7ddab24da65d42f", "tests/test_regex.py": "998a8bf99479ebbcf1b3a9dea10e5ad6fe089e2b55a3ecd6b4f2dda81b804a1e", "tests/test_string_component_transform_factory.py": "6a2843332cf00082c53df4f481fcfcdaa9089c8cc6fa837656df824fcc259d05", "tests/test_unicode_numbers.py": "ba4142319d02577ef7471a9ab9e55dcdea54225677d44fcbc3721f06eb9575f7", "tests/test_utils.py": "08166e4c12e7182da62b135f9f9837295837c1bc3f9efb0d583611dcf13600b9", "tox.ini": "dec616966b5dde7020b3f1bb86a28381d1b85d4b596a92a33a93887bfebb3bf1"}
JSON


%check
%{__python3} - "%{buildroot}%{_datadir}/python-natsort/original" "%{buildroot}%{python3_sitelib}" buildroot <<'PY'
import hashlib,importlib.abc,importlib.machinery,json,os,pathlib,re,shutil,subprocess,sys,tempfile
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text())
runtime={p.removeprefix('natsort/'):h for p,h in manifest.items() if p.startswith('natsort/')}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%%{NAME}',str(p)],text=True)=='python-natsort'
assert len(manifest)==62 and len(runtime)==12
for p,h in manifest.items():
    q=original/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
for p,h in runtime.items():
    q=site/'natsort'/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
if installed:
    archive=original.parent/'python-natsort-8.4.0.tar.gz';assert digest(archive)=='f0fdff4da8b535f475eed4b49d1942f787595558983a43a361ce9e68c3378b44';owned(archive);owned(original.parent/'original-files.json')
# Only RPM-generated Python caches of explicitly retained .py files may be extra.
for base,expected in ((original,manifest),(site/'natsort',runtime)):
    for p in base.rglob('*'):
        if not p.is_file():continue
        rel=p.relative_to(base).as_posix()
        if rel in expected:continue
        assert p.parent.name=='__pycache__' and p.suffix=='.pyc' and any(p.name.startswith(pathlib.Path(x).stem+'.') and p.parent.parent==base/pathlib.Path(x).parent for x in expected if x.endswith('.py')),rel
        owned(p)
guard="""import hashlib,importlib.abc,importlib.machinery,json,pathlib,sys
site=pathlib.Path(SITE_JSON).resolve();expected=json.loads(RUNTIME_JSON)
class OriginGuard(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname=='natsort' or fullname.startswith('natsort.'):
            spec=importlib.machinery.PathFinder.find_spec(fullname,path);assert spec and spec.origin
            p=pathlib.Path(spec.origin).resolve();rel=p.relative_to(site/'natsort').as_posix()
            assert rel in expected and hashlib.sha256(p.read_bytes()).hexdigest()==expected[rel],(fullname,str(p))
            return spec
        return None
sys.meta_path.insert(0,OriginGuard())
# Do not preload runtime before the original pytest-cov instrumentation starts.
""".replace('SITE_JSON',repr(str(site))).replace('RUNTIME_JSON',repr(json.dumps(runtime)))
with tempfile.TemporaryDirectory(prefix='python-natsort-defaults-') as scratch:
    work=pathlib.Path(scratch)/'original';work.mkdir()
    for p in manifest:
        if p.startswith('natsort/'):continue
        dst=work/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/p,dst)
    assert not (work/'natsort').exists()
    env=dict(os.environ,PYTHONPATH=str(site),PYTHONDONTWRITEBYTECODE='1');env.pop('WITH_EXTRAS',None)
    selected=[('doctest',['-o','IGNORE_EXCEPTION_DETAIL','docs/howitworks.rst']),('pytest',['README.rst','docs/examples.rst']),('pytest',['--doctest-modules',str(site/'natsort')]),('pytest',['--hypothesis-profile=slow-tests','--tb=short','--cov',str(site/'natsort'),'--cov-report','term-missing']),('coverage',['xml'])]
    for module,args in selected:
        code=guard+'\nimport runpy\nsys.argv='+repr([module]+args)+'\nrunpy.run_module('+repr(module)+',run_name="__main__")\n'
        subprocess.run([sys.executable,'-c',code],cwd=work,env=env,check=True)
    print(json.dumps({'route':'original GitHub Python3.11 -> tox py311, no extras','original_files':len(manifest),'runtime_files':len(runtime),'commands':selected,'runtime_origin':str(site/'natsort'),'engine':'installed-RPM' if installed else 'buildroot-wheel','boundary':'Original skips/configs preserved; no claim about other interpreter/extras/static jobs or performance.'}))
PY

%files
%license LICENSE
%doc README.rst CHANGELOG.md
%{python3_sitelib}/natsort/
%{python3_sitelib}/natsort-*.dist-info/
%{_bindir}/natsort
%{_datadir}/python-natsort/

%changelog
* Mon Oct 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 8.4.0-1
- Initial package with complete original selected Python 3.11 defaults.
