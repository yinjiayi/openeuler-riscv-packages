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
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%{NAME}',str(p)],text=True)==owner
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
