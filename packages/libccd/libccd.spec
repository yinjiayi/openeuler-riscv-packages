# SPDX-License-Identifier: Apache-2.0
# Static archive and headers only: no installed ELF for a debuginfo subpackage.
%global debug_package %{nil}
Name:           libccd
Version:        2.1
Release:        2%{?dist}
Summary:        Convex collision detection with default static double precision
License:        BSD-3-Clause AND LGPL-3.0-or-later
URL:            https://github.com/danfis/libccd
Source0:        libccd-2.1.tar.gz
Patch0:         0001-regressions-python3.patch
BuildRequires:  gcc make m4 glibc-devel python3 diffutils bash coreutils rpm patch gzip tar
Requires:       bash python3 rpm
Provides:       libccd-static = %{version}-%{release}
ExclusiveArch:  riscv64

%description
Collision detection between convex shapes using GJK and MPR. This package
follows upstream's first, plain-Make build: static library, default double
precision and every installed public header. CMake/autotools shared builds
are separate optional build systems and are not claimed here.
Pristine corresponding sources and complete BSD/GPL/LGPL notices are included.
The CU regression checker has only a Python 3 compatibility port.

%prep
%setup -q -n libccd-7931e764a19ef6b21b443376c699bbc9c6d4fba8
%autopatch -p1

%build
# Preserve default USE_DOUBLE=yes, USE_SINGLE=no and static TARGETS.
make -C src all CC=gcc

%install
make -C src install PREFIX=%{buildroot}%{_prefix} INCLUDEDIR=include LIBDIR=lib64
install -d %{buildroot}%{_datadir}/libccd
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/libccd/libccd-2.1.tar.gz
install -m 0644 %{PATCH0} %{buildroot}%{_datadir}/libccd/0001-regressions-python3.patch
cat > %{buildroot}%{_datadir}/libccd/original-files.json <<'JSON'
{
  ".gitignore": "9f2e831a28f824a1af90762a0a8aa6ef41ca0358e6deab0ec3597a319c5f4c7b",
  ".travis.yml": "02c4a95974b7bac20cd913b743b9445b8366ea87a1526a04221b6e13d81ec4ab",
  "BSD-LICENSE": "b175a981bfccf7e1e6c2f6fbda3fde0827aaa51808a983b10c8c7e6183c44a11",
  "CMakeLists.txt": "a252935fa1375dc1bb2ffe81a41bf9a454bdf5fd864618fe5cc2f4293a4cabeb",
  "Makefile.am": "cb6899ab93e0972f185c948aeadf62d6251b005a8d49a165ed6d4067f5f0e069",
  "README.md": "258f7262e7be8f09fb9d0a09ddd38a95acfdc9d6288d7ba449ff05775a5e1218",
  "bootstrap": "738e4e46971cf8f909c2e1037afb0f68b97fb534b6910df41a6e1ccf61704c95",
  "ccd-config.cmake.in": "53a14fb88d9945a4281bfd8e3c23b60beb3936c0cf2d1ae0c5d72dc2d22030e2",
  "ccd.pc.in": "086f05a32cce0c39d84d6689f2bd696f8dcdb538e17bf3fa0394a0fe8858f219",
  "configure.ac": "f1139f6b3c8416ca5293cf3a59c554fd7c14007a4c0d6eea17789e98aa8c3383",
  "doc/CMakeLists.txt": "299669f66567d857251a5160d959aef5228d8eabf63725582a41b98e30ddcd72",
  "doc/Makefile": "145b9b206fefba05955cbd0ad25bc7bf5376600923521a8ab77486a5e58afad9",
  "doc/_build/.dir": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "doc/_static/.dir": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "doc/_templates/.dir": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "doc/compile-and-install.rst": "2bf076ea2fe6b52bfde99e6d5e24fd0f32a1bf1970cff8aaad0f486e8980375b",
  "doc/conf.py": "7ce541cff54c4fe1ca4b22f3ded8d0eb0d3cf7956ced62c252e7b223b631ee27",
  "doc/examples.rst": "0bd1c3df82bd7f60fe0f4fa92b8c2eb6bddb0f67ea738bca8dd4f5d8c8b20205",
  "doc/index.rst": "8613231e62b166ce5a791e13e5a3f9b21000fc48840dc7ff34c2e54525b49cd8",
  "doc/reference.rst": "c8b74de6627a4e7dd0f76a374caa356fff4e35a55583ad35966dd239561ae0e7",
  "make-release.sh": "a1a846c1652dce253380153540ee9e8fcd807d26c5f22fe7e29adfb324434ee8",
  "src/.gitignore": "363902ad58ed9ebb8f80c41e3b42fcade96496a9f43e0f64733c1b3823cea523",
  "src/CMakeLists.txt": "d64a0c611e90a1bfd2caca7a033d1f7e11e74ecb0cc3bb1173243a3c0379849c",
  "src/Makefile": "d7d2912437060047f7808dab52e19c3c780a2ef0e327cefdcb7bc94fcc100546",
  "src/Makefile.am": "6ee4bd08c4a2fd719c3917f22c3af54f44d414921d3c8f2c594b7f96e0e16316",
  "src/Makefile.include": "1df2669ad36b0289c91c142ad45fab090670d17e92103a8e396394492bfec4d7",
  "src/alloc.h": "841b8086dd72edfd095ee6068bed6877c3580e7f2754c90ad61270a8c984cba1",
  "src/ccd.c": "92a55f1f807082f144f9b5b2f45ee8797a1d2b40ce75aa5a082714dd798b6780",
  "src/ccd/ccd.h": "fff1ef9b45bb5c73ff09eecd54c61196b9b0cef2a0fff90b168b63b29769a350",
  "src/ccd/ccd_export.h": "1dcda955b7d21e58fdd6f313b55ced7329c94e97bf53ea67ade9a32e8a419f3f",
  "src/ccd/compiler.h": "51ecb05280ff5e857f1cd74247d95b15d4eebc2a4f543f0322b802a49ea43f8b",
  "src/ccd/config.h.cmake.in": "99de5ae050ef2d33deac2e645fc0cb0365d7d4443a915a4307dbd420799f3808",
  "src/ccd/config.h.m4": "40c412ded2d9c7abd0702005b42cc81bdbf5958679acec8152a1c13781e8f699",
  "src/ccd/quat.h": "fd59e18aefc7d7329a2d9ec9069d5f2c1ceadc3c40def59f56d5d27d5a0fc8c4",
  "src/ccd/vec3.h": "89c4b4e52ec27f24108a6ff18a65879bd6ad31475ebbaf712488220ee5369934",
  "src/dbg.h": "f07463e5e4c097d9f6413aa04efe6ad3bf9a248f500d0d69282e8e50cfede184",
  "src/list.h": "471b2ac6b936d9d7c8c68c49d470c9ed09ab28b6398621224d428cab3c44e4ce",
  "src/mpr.c": "770971cfb36763082e93e9a3ab93fd2ff0ec57c136f4fcce5cb2bff033c01a08",
  "src/polytope.c": "9f8c7913aa33cfbb33fc647a387bd7e6934f594d65170f75007c489dd87790dc",
  "src/polytope.h": "80501ed958ab7d27772432b63a597cf76bbc1a684077e74e24ee6c81f95486a0",
  "src/simplex.h": "6aa5dc4e5e4bcac7f4c744153d42fc907af22f7bf9f2f34eecb0a6394cc374f9",
  "src/support.c": "f4633616738238264cd753fa15f02526601a5210d978fdd191abbbc1786e51c0",
  "src/support.h": "b044ec72f4906cdbab124467565cfa06ef88cb145d6aa53afc62ed8e9d2a483e",
  "src/testsuites/.gitignore": "ffacd5f7c0326d55811b3ae7006322e85e642bc668081ccd3079c904d618afe1",
  "src/testsuites/CMakeLists.txt": "5e5e796cb495c7502d97ac6b285541a9fcdcc6b6ad479bb202b7019fe510a78c",
  "src/testsuites/Makefile": "b93775016e1794aab0298c99c5d25c02afcc152adc3d2241c7c5cb65d542c1b2",
  "src/testsuites/Makefile.am": "4a885274e31170cda941a1322a3c502eea0c7c2bcb334f81cc2204a1c7a1224c",
  "src/testsuites/bench.c": "94b003d38f3edff85f4c6c017a8db7edc4693512c9a0e7ae15334b387cd5285b",
  "src/testsuites/bench2.c": "e2d4a0f45ef206787606658a729a02090f66bcbd3cc548c9315576c12a0556ea",
  "src/testsuites/boxbox.c": "e5d60563bc261bc74d7bafd8fc5be68b4af1339095db803a957529a24963dc20",
  "src/testsuites/boxbox.h": "80dd78e26e50d8d3e51abe5ceaf297f8b4ff51c197b925c8d86a233fab0df7a8",
  "src/testsuites/boxcyl.c": "ba8ca5d948c380649e25e24acb69f5e58ada8bc15a19209e1245941ef87a622f",
  "src/testsuites/boxcyl.h": "febaf2036b3b09604080576675812f83341da1ea41daf961a8f6cc3e5c07c194",
  "src/testsuites/common.c": "a1f5bc81cbb66fbdf8b2ddfab79bf5d78b19a3f37b5a5acf7262d6f1dc00b773",
  "src/testsuites/common.h": "485f2e8cd9ed44d4520e7c7dd431f9de3f49efbccdcd0b17238533dc97b9a8e8",
  "src/testsuites/cu/.dir": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "src/testsuites/cu/.gitignore": "f7850f23ac1766fee47e781115addb5b3fef4a84dcfa8a1c802f069497000f2d",
  "src/testsuites/cu/CMakeLists.txt": "ccb204ea92b147a8e9ee1d34a8a8ce14638e42c21ae7502e753bac780d763138",
  "src/testsuites/cu/COPYING": "8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903",
  "src/testsuites/cu/COPYING.LESSER": "a853c2ffec17057872340eee242ae4d96cbf2b520ae27d903e1b2fef1a5f9d1c",
  "src/testsuites/cu/Makefile": "ef3d199ccd7072354c05b455e1d777ca052742661ded25eb980f5c3a179048d4",
  "src/testsuites/cu/Makefile.am": "38519ead1ad6e6e04d46c52685a0719918fac1f59b06e151874beb101cd520d2",
  "src/testsuites/cu/check-regressions": "060bc5df6230b0ce64728f0af097878856faf407d50b12fd5f978676fcb56224",
  "src/testsuites/cu/cu.c": "5ed72172e478cfaf66e06b26d525519dedec729594906e946d1f206c3446b7b7",
  "src/testsuites/cu/cu.h": "96616c0776c13df0a91c2ef0d93532a34e549ab5d23c6fb466784e4c4a1da9dd",
  "src/testsuites/cu/latest.sh": "9e764cbb74c44bd21daffd4552884d52028ca766fc157249115733e75f3e8b1a",
  "src/testsuites/cylcyl.c": "bb6d4e0abc510a9dfa5b0a6cfeaf938f5823c7a65e31360c8c01b4e2b9bcfa4f",
  "src/testsuites/cylcyl.h": "7883bdaee16b42f1745208943de9d54c113ae0efb7af2755ae7eb4a905675fbc",
  "src/testsuites/main.c": "5c7ca336f1f22fa3000453ff4150fc1870ce677c7cc6989d1c729054c9280729",
  "src/testsuites/mpr_boxbox.c": "86424058e8604bcce1daf02a33eef21dca2f03b60b95f64d0bca2db4307165e6",
  "src/testsuites/mpr_boxbox.h": "89d2ae74e6799aa5c5df04c4ea0e10fc0c4e54117beea10387c6a062589c3dcb",
  "src/testsuites/mpr_boxcyl.c": "fcba42e3005bf362cccdfe23242c2daa6559d7a5f4371c0e9233147da4861a57",
  "src/testsuites/mpr_boxcyl.h": "0771908f62c0208c66d53fdf1e01b95d3e6b7bdd0752a4a45dead7c4145c231c",
  "src/testsuites/mpr_cylcyl.c": "19e8838bea7c6a9949466a2ad66d4f778574b6e2c094dd23f37c8fabff45ef1f",
  "src/testsuites/mpr_cylcyl.h": "db4f021d56ababd0f4c8f6bc2ed12f22a7475ce50fdb5271dd30bcf45e59dabc",
  "src/testsuites/polytope.c": "76796dc8349d3294aabc32597aad2b7da77f17367120b445f80b683917178664",
  "src/testsuites/polytope.h": "a2af78f035867131f942dd1caaef0ccc235f96e67007aca827ae69439c2d89d0",
  "src/testsuites/regressions/.dir": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "src/testsuites/regressions/TSBoxBox.err": "dfd8afffafcb316f770a06de6806fa94cb070f3287a0080dc497c42eb61b8912",
  "src/testsuites/regressions/TSBoxBox.out": "a22f2d5fa2323a93d450f09f7cf895dd43ae31b17eb742000ef1360330607ddc",
  "src/testsuites/regressions/TSBoxCyl.err": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "src/testsuites/regressions/TSBoxCyl.out": "a538dff6ebe4efccc9a80d81ee61890d15af1aff2fe0423a31701e3b54dbda93",
  "src/testsuites/regressions/TSCylCyl.err": "d05327f3e7dce71fe005154ffe1068e40d894365d3647cf8284820e63e8fe6e6",
  "src/testsuites/regressions/TSCylCyl.out": "a201e786258c88acf85afc77fff7351b01cbb63141e80732b63c92aaedccbfe1",
  "src/testsuites/regressions/TSMPRBoxBox.err": "dfd8afffafcb316f770a06de6806fa94cb070f3287a0080dc497c42eb61b8912",
  "src/testsuites/regressions/TSMPRBoxBox.out": "c70fccccd52b8299bcebdef18b3a9b81003d4882afac6856c70466e6b7ad6dea",
  "src/testsuites/regressions/TSMPRBoxCyl.err": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "src/testsuites/regressions/TSMPRBoxCyl.out": "46105e297dd42c390305e95c456ba3146ccda18f0bb2e822d447d9f168503020",
  "src/testsuites/regressions/TSMPRCylCyl.err": "4c5cc3d87a01c5ba6cd8d063e135c1cd028c374e11e9289e2101fd1213c0c537",
  "src/testsuites/regressions/TSMPRCylCyl.out": "f57bb08841b9bea4e80295d7bf3c76bc8a91bc21fca7afd6b0b7b6f9c71b9d26",
  "src/testsuites/regressions/TSPt.err": "900167c67c0057585c867415d8a7eff93b05a74a7f9a97aa532b26417b9f2b7b",
  "src/testsuites/regressions/TSPt.out": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "src/testsuites/regressions/TSSphereSphere.err": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "src/testsuites/regressions/TSSphereSphere.out": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "src/testsuites/regressions/TSVec3.err": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "src/testsuites/regressions/TSVec3.out": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "src/testsuites/spheresphere.c": "3af39e1271c93a132b8f212eef94bd46054cc23dfd678cdec7a7e12923093ba2",
  "src/testsuites/spheresphere.h": "bfcc471b645c1b28869933e985198be5ec414cfa5c94a1aed3456079017adc78",
  "src/testsuites/support.c": "198fa6b398cb68d6001586ab6c1142115bd811dab5c3454168d232fa6edbbadd",
  "src/testsuites/support.h": "24f7a74a1158f181e9f1228c87ad1f5883d7e72aa9e6fb25acecfff98cec575f",
  "src/testsuites/vec3.c": "235a2751b250fa42d4cff3922278242df795c68092b228d48609976ea745a046",
  "src/testsuites/vec3.h": "240ff884e94f7dc0c3905d0bcda08ec77050779a95cd1dfd8bb16eb2c5b790d2",
  "src/vec3.c": "b93478e963a32f902f7ddf48696ecf358a4551ac4de56c3684093fb55490284e"
}
JSON
cat > %{buildroot}%{_datadir}/libccd/verify-defaults.sh <<'SH'
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
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%%{NAME}',str(p)],text=True)=='libccd'
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
SH
chmod 0755 %{buildroot}%{_datadir}/libccd/verify-defaults.sh

%check
# Original make check, all nine suites/42 test entries/18 regression pairs,
# then unchanged default suites compiled against staged RPM public headers
# and the exact staged static archive. No CHECK_TS filter or weaker epsilon.
bash %{buildroot}%{_datadir}/libccd/verify-defaults.sh %{buildroot}%{_datadir}/libccd %{buildroot} staged "$(pwd)"

%files
%license BSD-LICENSE src/testsuites/cu/COPYING src/testsuites/cu/COPYING.LESSER
%doc README.md doc/*.rst
%{_includedir}/ccd/
%{_libdir}/libccd.a
%{_datadir}/libccd/

%changelog
* Thu Oct 15 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1-1
- Preserve upstream plain-Make defaults and full original regression suite.
- Port CU checker to Python 3 without changing comparison rules or tolerance.
- Enforce complete zero-failure summaries and actual RPM-bound install checks.
