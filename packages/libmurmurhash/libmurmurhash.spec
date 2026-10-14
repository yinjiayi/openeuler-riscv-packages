# SPDX-License-Identifier: Apache-2.0
Name:           libmurmurhash
Version:        1.6
Release:        1%{?dist}
Summary:        Portable MurmurHash3 shared library
License:        LicenseRef-Public-Domain
URL:            https://github.com/kloetzl/libmurmurhash
Source0:        libmurmurhash-1.6.tar.gz
Patch0:         0001-pkgconfig-use-configured-libdir.patch
BuildRequires:  autoconf >= 2.57
BuildRequires:  automake >= 1.6
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  gzip
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  patch
BuildRequires:  pkgconf
BuildRequires:  python3
BuildRequires:  rpm
BuildRequires:  sed
BuildRequires:  tar

%description
Portable non-cryptographic MurmurHash3 implementation with current and
deprecated C interfaces. No architecture-specific acceleration is assumed.

%package devel
Summary:        Headers and static library for Libmurmurhash
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Public headers, shared-library linker name, the original default static
library, pkg-config metadata and manual. All 17 upstream originals, their
checksum manifest and fixed source archive are retained for installed
default dynamic-library and deprecated-ABI origin verification. Compiler
and Autotools test support is installed separately by the protected smoke
transaction, not required by consumers.

%prep
%setup -q -n libmurmurhash-8b7c9bf3ed1b8f83e5265c84a2cad5c1d6bb1d69
test ! -e ../libmurmurhash-pristine
mkdir ../libmurmurhash-pristine
cp -a . ../libmurmurhash-pristine/
%patch0 -p1

%build
autoreconf -fi
%configure
%make_build

%install
%make_install
find %{buildroot}%{_libdir} -name '*.la' -type f -delete
install -d %{buildroot}%{_datadir}/libmurmurhash/original
cp -a ../libmurmurhash-pristine/. %{buildroot}%{_datadir}/libmurmurhash/original/
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/libmurmurhash/libmurmurhash-1.6.tar.gz
cat > %{buildroot}%{_datadir}/libmurmurhash/original-files.json <<'JSON'
{".gitignore":"18eac0cc8e70bd2c1aec82798494d195b0f7eb994ac901683d670367987c9d5f","Makefile.am":"ecd2b9c42e9628d5d2aaeea35ebc8479695e3fe043fd8afc73c1a2927195ad23","NOLICENSE":"fde096c48cbd3dfd0c90a7e34e462ee38a638a263a232ee3e180f9f202d6450c","PMurHash.c":"891a74d8a747b74daf7faefadcfb3df8a7f72e4cae227bfdd8cb34cfbc2cb2ef","PMurHash.h":"1303f86f25bb4aebc1fe9f77ff918b983d9884de50d46ded05e51c59706c4685","Readme.md":"f803faf970b75b99e8384494b9e8868171d9b4c8f69ab0f6a6864afe3a5c39d5","configure.ac":"a32ee42606b4fd65d32306810504324a2793a37e9c36f7d5da7ab6b77dda6d30","libmurmurhash.pc.in":"686b607ba90b3c8b2f872ccc02ff9f8abf802f5f6a2a706b325ba3785756115f","murmurhash.3":"b32ab67cba09c15aef5359d7b1284955ead32c9aa3a3cacc6ea483fc4562f3cf","murmurhash.c":"8541fc230d7369ff9c695f945f5053f1a526d3bbdd20b89bb164762a56021856","murmurhash.h":"f5bf3009ee644332cf6db2eec56bb2ccf9bc1ace18dd1f7285ceec637afb5101","test/MurmurHash3.c":"75ba7f318b4ddf468d323aec7311a34e43ea636c3d021840c297c9fc8f8cf969","test/MurmurHash3.h":"dcfa9d304f0bb4f1d9202c78235abeea8724cea1295408142e5126d6aa7ffefe","test/almostempty":"b72720feead6cb13ef4cb1fb04b7c440e1ed409a2fd1d88d74ed4a1ce29ab19c","test/almostempty.hash":"0a3dda70045109d29b56c06fa17da3d89eeb0cce744ef785844328ccb6a4ebde","test/mmh.c":"f7f3c6f5d36b8133abbd61968de4ad024a5d4d4ebef4cd08d9710db5ad8099f2","test/mmh_old.c":"8712b5a3bae5c28261aaa6af7e06d61ee05876571022d8669ca3990490355ec3"}
JSON

%check
# Preserve both original check recipes; producer failures cannot hide behind diff.
%make_build SHELL=/bin/bash '.SHELLFLAGS=-e -o pipefail -c' check
cat > libmurmurhash-origin.sh <<'SH'
#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail
if [[ ${3:-installed} == installed ]]; then
  rpm -q -- libmurmurhash libmurmurhash-devel
  [[ $(pwd -P) == /workspace && -f artifacts/repository/resolution.json ]]
  if [[ -d artifacts/smoke ]]; then test_evidence_dir=artifacts/smoke; elif [[ -d artifacts/golden/libmurmurhash ]]; then test_evidence_dir=artifacts/golden/libmurmurhash; else exit 2; fi
  [[ ! -e $test_evidence_dir/libmurmurhash-test-prerequisites.json ]]
  printf 'd62f6ec90fa3a5c5112ad4cd364d7a75ef69778c2a432825add4164a1bd64eca  ci/run-dnf-transaction\n' | sha256sum --check --strict
  # Test-support tools only; not consumer dependencies and never replace candidate RPMs.
  python3 ci/run-dnf-transaction --evidence "$test_evidence_dir/libmurmurhash-test-prerequisites.json" --budget-seconds 900 --attempt-timeouts-seconds 890 --retry-delay-seconds 0 --kill-after-seconds 10 -- dnf -y --setopt=install_weak_deps=False --disablerepo='*' --enablerepo=openeuler-rva23 install -- autoconf automake binutils coreutils diffutils gcc glibc-devel libtool make pkgconf python3 bash rpm findutils gzip tar patch sed grep
fi
python3 -I - "${1:-/usr/share/libmurmurhash}" "${2:-}" "${3:-installed}" <<'PY'
import hashlib,json,os,pathlib,re,shutil,subprocess,sys,tempfile
base=pathlib.Path(sys.argv[1]).resolve()
stage=pathlib.Path(sys.argv[2]).resolve() if sys.argv[2] else None
installed=sys.argv[3]=='installed'
assert installed != (stage is not None)
original=base/'original'
manifest=json.loads((base/'original-files.json').read_text())
assert len(manifest)==17
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p,owner):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%%{NAME}',str(p)],text=True)==owner
def physical(p):
    assert p.is_file() and not p.is_symlink()
    if stage is not None:p.resolve().relative_to(stage)
    return p.resolve()
assert {p.relative_to(original).as_posix() for p in original.rglob('*') if p.is_file()}==set(manifest)
for rel,h in manifest.items():
    p=physical(original/rel);assert digest(p)==h;owned(p,'libmurmurhash-devel')
for p in (base/'original-files.json',base/'libmurmurhash-1.6.tar.gz'):
    physical(p);owned(p,'libmurmurhash-devel')
assert digest(base/'libmurmurhash-1.6.tar.gz')=='6942827223d228c7a5efb791e6300d0cede1fa290815c79dd8f11957db5dc32b'
libdir=(stage/'usr/lib64') if stage is not None else pathlib.Path('/usr/lib64')
includedir=(stage/'usr/include') if stage is not None else pathlib.Path('/usr/include')
header=physical(includedir/'murmurhash.h');assert digest(header)==manifest['murmurhash.h'];owned(header,'libmurmurhash-devel')
library=(libdir/'libmurmurhash.so.2').resolve()
assert library.parent==libdir.resolve() and physical(library)==library
library_hash=digest(library);owned(library,'libmurmurhash')
assert (libdir/'libmurmurhash.so').resolve()==library;owned(libdir/'libmurmurhash.so','libmurmurhash-devel')
static=physical(libdir/'libmurmurhash.a');static_hash=digest(static);owned(static,'libmurmurhash-devel')
pc=physical(libdir/'pkgconfig/libmurmurhash.pc');owned(pc,'libmurmurhash-devel')
pc_text=pc.read_text();assert re.search(r'^libdir=/usr/lib64$',pc_text,re.M)
assert re.search(r'^Version: 1\.6$',pc_text,re.M) and re.search(r'^Libs: -L\$\{libdir\} -lmurmurhash$',pc_text,re.M)
env=dict(os.environ,LC_ALL='C',LD_LIBRARY_PATH=str(libdir),CPPFLAGS='-I'+str(includedir),LDFLAGS='-L'+str(libdir))
for key in list(env):
    if key.startswith('LD_') and key!='LD_LIBRARY_PATH':env.pop(key,None)
for key in ('LIBRARY_PATH','CPATH','C_INCLUDE_PATH','CPLUS_INCLUDE_PATH','GCC_EXEC_PREFIX','COMPILER_PATH','CONFIG_SITE','MAKEFLAGS','MFLAGS','CFLAGS','CC','PKG_CONFIG_PATH','PKG_CONFIG_SYSROOT_DIR','PKG_CONFIG_LIBDIR'):
    env.pop(key,None)
commands=[];traces=[]
def run(args,cwd,extra=None):
    e=dict(env);e.update(extra or {})
    p=subprocess.run(args,cwd=cwd,env=e,capture_output=True,text=True)
    print(p.stdout,end='');print(p.stderr,end='',file=sys.stderr)
    commands.append(dict(argv=args,returncode=p.returncode,stdout_sha256=hashlib.sha256(p.stdout.encode()).hexdigest(),stderr_sha256=hashlib.sha256(p.stderr.encode()).hexdigest()))
    p.check_returncode();return p
def origin(binary,work):
    assert binary.is_file() and binary.read_bytes()[:4]==b'\x7fELF'
    dt=run(['readelf','-d',str(binary)],work).stdout
    needed=re.findall(r'\(NEEDED\).*?\[([^]]+)\]',dt)
    assert [x for x in needed if 'murmurhash' in x]==['libmurmurhash.so.2']
    output=run(['ldd',str(binary)],work).stdout
    matches=re.findall(r'^\s*libmurmurhash\.so\.2\s+=>\s+(\S+)',output,re.M)
    assert len(matches)==1 and pathlib.Path(matches[0]).resolve()==library and digest(library)==library_hash
    return dict(binary=str(binary),binary_sha256=digest(binary),library=str(library),library_sha256=library_hash)
with tempfile.TemporaryDirectory(prefix='libmurmurhash-installed-defaults-') as tmp:
    work=pathlib.Path(tmp)/'original';shutil.copytree(original,work)
    run(['autoreconf','-fi'],work)
    run(['./configure','--prefix=/usr','--libdir=/usr/lib64'],work)
    # Pristine RPM-owned originals remain unchanged; only scratch runtime/header
    # copies are removed to preclude source header or local-library fallback.
    for rel in ('murmurhash.h','murmurhash.c','PMurHash.h','PMurHash.c'):(work/rel).unlink()
    make=['make','SHELL=/bin/bash','.SHELLFLAGS=-e -o pipefail -c']
    run(make+['mmh_dyn'],work)
    binaries=[p for p in (work/'.libs/mmh_dyn',work/'mmh_dyn') if p.is_file() and p.read_bytes()[:4]==b'\x7fELF']
    assert len(binaries)==1 and not list(work.rglob('libmurmurhash.so*')) and not list(work.rglob('libmurmurhash.a'))
    traces.append(origin(binaries[0],work))
    result=run(make+['check-dynamic'],work,dict(LD_DEBUG='libs'))
    loaded=re.findall(r'calling init:\s*(\S*libmurmurhash\.so\.2\S*)',result.stderr)
    assert loaded and all(pathlib.Path(p).resolve()==library for p in loaded)
    # Extra deprecated installed ABI check; does not replace original defaults.
    legacy=work/'installed-mmh-old'
    run(['gcc','-I'+str(includedir),str(work/'test/mmh_old.c'),'-L'+str(libdir),'-lmurmurhash','-o',str(legacy)],work)
    traces.append(origin(legacy,work))
    legacy_result=run([str(legacy),str(work/'test/almostempty')],work,dict(LD_DEBUG='libs'))
    assert legacy_result.stdout.encode()==(original/'test/almostempty.hash').read_bytes()
    loaded_old=re.findall(r'calling init:\s*(\S*libmurmurhash\.so\.2\S*)',legacy_result.stderr)
    assert loaded_old and all(pathlib.Path(p).resolve()==library for p in loaded_old)
for rel,h in manifest.items():assert digest(original/rel)==h
assert digest(library)==library_hash and digest(static)==static_hash
print('LIBMURMURHASH_DEFAULT_RESULT='+json.dumps(dict(mode='installed-RPM' if installed else 'staged-RPM',original_files=17,commands=commands,origins=traces,static_library_sha256=static_hash,original_dynamic_target='make check-dynamic',boundary='Unmodified build-time make check new/deprecated ABI plus installed check-dynamic; separate x86-only check-ref retained and unclaimed. No local candidate execution.')))
PY
SH
/bin/bash libmurmurhash-origin.sh "%{buildroot}%{_datadir}/libmurmurhash" "%{buildroot}" staged

%files
%license NOLICENSE
%doc Readme.md
%{_libdir}/libmurmurhash.so.2*

%files devel
%{_includedir}/murmurhash.h
%{_libdir}/libmurmurhash.so
%{_libdir}/libmurmurhash.a
%{_libdir}/pkgconfig/libmurmurhash.pc
%{_mandir}/man3/murmurhash.3*
%{_datadir}/libmurmurhash/

%changelog
* Wed Oct 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6-1
- Retain both original default ABI checks and installed dynamic target.
- Preserve default static library and complete public-domain originals.
- Use configured libdir in pkg-config metadata.
