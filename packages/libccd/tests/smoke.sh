#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail
if [[ ${3:-installed} == installed ]]; then
  rpm -q -- libccd
  [[ $(pwd -P) == /workspace && -f artifacts/repository/resolution.json ]]
  if [[ -d artifacts/smoke ]]; then test_evidence_dir=artifacts/smoke; elif [[ -d artifacts/golden/libccd ]]; then test_evidence_dir=artifacts/golden/libccd; else exit 2; fi
  [[ ! -e $test_evidence_dir/libccd-test-prerequisites.json ]]
  printf 'd62f6ec90fa3a5c5112ad4cd364d7a75ef69778c2a432825add4164a1bd64eca  ci/run-dnf-transaction\n' | sha256sum --check --strict
  # Only isolated test support; never replace the candidate RPM or add consumer dependencies.
  python3 ci/run-dnf-transaction --evidence "$test_evidence_dir/libccd-test-prerequisites.json" --budget-seconds 900 --attempt-timeouts-seconds 890 --retry-delay-seconds 0 --kill-after-seconds 10 -- dnf -y --setopt=install_weak_deps=False --disablerepo='*' --enablerepo=openeuler-rva23 install -- gcc make m4 glibc-devel python3 diffutils bash coreutils rpm patch gzip tar
fi
python3 -I - "${1:-/usr/share/libccd}" "${2:-}" "${3:-installed}" "${4:-}" <<'PY'
import hashlib,json,os,pathlib,re,shutil,subprocess,sys,tarfile,tempfile
base=pathlib.Path(sys.argv[1]).resolve()
stage=pathlib.Path(sys.argv[2]).resolve() if sys.argv[2] else None
installed=sys.argv[3]=='installed'
source=pathlib.Path(sys.argv[4]).resolve() if sys.argv[4] else None
assert sys.argv[3] in ('installed','staged') and installed != (stage is not None)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    assert p.is_file() and not p.is_symlink()
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%{NAME}',str(p)],text=True)=='libccd'
    else:p.resolve().relative_to(stage)
archive=base/'libccd-2.1.tar.gz';port=base/'0001-regressions-python3.patch';manifest_path=base/'original-files.json'
for p in (archive,port,manifest_path,base/'verify-defaults.sh'):owned(p)
assert digest(archive)=='479994a86d32e2effcaad64204142000ee6b6b291fd1859ac6710aee8d00a482'
manifest=json.loads(manifest_path.read_text());assert len(manifest)==103
port_hash=digest(port)
libdir=stage/'usr/lib64' if stage else pathlib.Path('/usr/lib64')
include=stage/'usr/include' if stage else pathlib.Path('/usr/include')
library=libdir/'libccd.a';owned(library);library_hash=digest(library)
headers={p.name:digest(p) for p in (include/'ccd').glob('*.h')}
expected_headers={pathlib.Path(k).name:v for k,v in manifest.items() if k.startswith('src/ccd/') and k.endswith('.h')}
assert set(headers)==set(expected_headers)|{'config.h'}
for name,h in expected_headers.items():owned(include/'ccd'/name);assert headers[name]==h
config=include/'ccd/config.h';owned(config)
assert re.search(r'^#define CCD_DOUBLE\b',config.read_text(),re.M) and not re.search(r'^#define CCD_SINGLE\b',config.read_text(),re.M)
env=dict(os.environ,LC_ALL='C')
for key in list(env):
    if key.startswith('LD_'):env.pop(key,None)
for key in ('LIBRARY_PATH','CPATH','C_INCLUDE_PATH','CPLUS_INCLUDE_PATH','GCC_EXEC_PREFIX','COMPILER_PATH','MAKEFLAGS','MFLAGS','CFLAGS','CPPFLAGS','LDFLAGS','CC','CHECK_TS','PYTHONPATH','PYTHONHOME'):
    env.pop(key,None)
commands=[];results=[]
def run(args,cwd):
    p=subprocess.run(args,cwd=cwd,env=env,capture_output=True,text=True)
    print(p.stdout,end='');print(p.stderr,end='',file=sys.stderr)
    commands.append(dict(argv=args,returncode=p.returncode,stdout_sha256=hashlib.sha256(p.stdout.encode()).hexdigest(),stderr_sha256=hashlib.sha256(p.stderr.encode()).hexdigest()))
    p.check_returncode();return p
def validate(result,work,label):
    text=re.sub(r'\x1b\[[0-9;]*m','',result.stdout+'\n'+result.stderr)
    assert not re.search(r'FAILED|terminated by signal|terminated abnormal|Traceback|Can.t compare|does not exist|^diff:',text,re.M)
    totals={}
    for name,total in [('assertations',None),('tests',42),('tests suites',9)]:
        rows=re.findall(r'^\| '+name+r':\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|$',text,re.M)
        assert len(rows)==1,(name,rows)
        failed,succeeded,count=map(int,rows[0]);assert failed==0 and succeeded==count and count>0 and (total is None or count==total)
        totals[name]=count
    suites=['TSVec3','TSPt','TSBoxBox','TSSphereSphere','TSCylCyl','TSBoxCyl','TSMPRBoxBox','TSMPRCylCyl','TSMPRBoxCyl']
    assert sorted(re.findall(r' -> (\w+) \[DONE\]',text))==sorted(suites)
    reg=work/'src/testsuites/regressions'
    expected={pathlib.Path(k).name for k in manifest if k.startswith('src/testsuites/regressions/') and k.endswith(('.out','.err'))}
    assert len(expected)==18
    assert {p.name for p in reg.glob('tmp.*')}=={'tmp.'+x for x in expected}
    comparisons=re.findall(r'Comparing\s+tmp\.(\S+)\s+and\s+(\S+)\s+\[\s*OK\s*\]',text)
    assert len(comparisons)==18 and {a for a,b in comparisons if a==b}==expected
    for rel,h in manifest.items():
        if rel.startswith('src/testsuites/regressions/'):assert digest(work/rel)==h
    results.append(dict(mode=label,totals=totals,regression_pairs=18,default_epsilon=0.6,default_exact=False))
if source:
    # Original default target, no suite selection or tolerance override.
    validate(run(['make','-C','src','check','PYTHON=python3'],source),source,'original-source-default')
with tempfile.TemporaryDirectory(prefix='libccd-rpm-defaults-') as tmp:
    work=pathlib.Path(tmp)/'original';work.mkdir()
    with tarfile.open(archive) as tf:
        data={}
        for member in tf.getmembers():
            parts=pathlib.PurePosixPath(member.name).parts
            assert parts and not member.name.startswith('/') and '..' not in parts and (member.isdir() or member.isfile())
            if member.isfile():
                rel='/'.join(parts[1:]);assert rel in manifest and rel not in data
                blob=tf.extractfile(member).read();assert hashlib.sha256(blob).hexdigest()==manifest[rel];data[rel]=blob
        assert set(data)==set(manifest)
    for rel,blob in data.items():
        p=work/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(blob)
    run(['patch','--batch','--fuzz=0','-p1','-i',str(port)],work)
    # Only temporary copies: prevent any source header/static-library fallback.
    shutil.rmtree(work/'src/ccd')
    for name in ('ccd.c','mpr.c','support.c','vec3.c','polytope.c'):(work/'src'/name).unlink()
    assert not list(work.rglob('libccd.a'))
    flags='-g -Wall -pedantic --std=gnu99 -DCU_ENABLE_TIMER -I./ -I../ -Icu/ -I'+str(include)
    links='-Lcu/ -lcu '+str(library)+' -lrt -lm'
    validate(run(['make','-C','src/testsuites','check','PYTHON=python3','CC=gcc','CFLAGS='+flags,'LDFLAGS='+links],work),work,'installed-RPM-default' if installed else 'staged-RPM-default')
    assert not list(work.rglob('libccd.a')) and (work/'src/testsuites/test').read_bytes()[:4]==b'\x7fELF'
assert digest(library)==library_hash and digest(port)==port_hash
assert {p.name:digest(p) for p in (include/'ccd').glob('*.h')}==headers
print('LIBCCD_DEFAULT_RESULT='+json.dumps(dict(original_files=103,results=results,commands=commands,library=str(library),library_sha256=library_hash,patch_sha256=port_hash,boundary='Original plain-Make static/double default check, repeated against actual RPM archive/public headers. Bench binaries built, not executed by this default target; timing/performance/native and alternative CMake/autotools features unclaimed.')))
PY
