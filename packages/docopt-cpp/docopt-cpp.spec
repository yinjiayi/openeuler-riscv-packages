# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 openEuler RISC-V package contributors
Name:           docopt-cpp
Version:        0.6.3
Release:        1%{?dist}
Summary:        C++11 command-line parser shared and static SDK
License:        BSL-1.0 AND Apache-2.0
URL:            https://github.com/docopt/docopt.cpp
# Actual selected official release URL: https://api.github.com/repos/docopt/docopt.cpp/tarball/v0.6.3
Source0:        docopt-cpp-0.6.3-Git.tar.gz
# Official owned-QA legal text: https://www.apache.org/licenses/LICENSE-2.0.txt
Source1:        Apache-2.0.txt
Patch0:         0001-align-release-and-wire-original-python3-tests.patch
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  cmake >= 3.20
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  gcc-c++
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  gzip
BuildRequires:  make
BuildRequires:  patch
BuildRequires:  pkgconf
BuildRequires:  python3 >= 3.6
BuildRequires:  tar
Requires:       bash
Requires:       binutils
Requires:       cmake >= 3.20
Requires:       coreutils
Requires:       diffutils
Requires:       gcc-c++
Requires:       glibc-devel
Requires:       grep
Requires:       make
Requires:       pkgconf
Requires:       python3 >= 3.6

%description
The original C++11 docopt port as one deliberate shared/static SDK, including
its supplied headers, CMake exports and pkgconfig metadata. Select the explicit
whole-port Boost Software License offer and retain both original full grants.
No installed header-only route, native ABI or target success is claimed.

%prep
%setup -q -n docopt-docopt.cpp-42ebcec
python3 - <<'PY_ORIGINALS'
import hashlib,json,stat
from pathlib import Path
original = {'.gitignore': {'sha256': '7bd15d58d4d1dcfcf4ab3d5eef5c6e7c1fda902d4ae02e6bcb5f824b63de2fa2', 'bytes': 404, 'Git_mode': '100644'}, '.travis.yml': {'sha256': 'fd4f358a5580914c47f08aeb0211b3b657298f6f551b7940554428ba1ce3d315', 'bytes': 2928, 'Git_mode': '100644'}, 'CMakeLists.txt': {'sha256': '40ee78167eca21764ea234465d505aa25c3f57c5f0b86942ced7c16266757bd5', 'bytes': 6480, 'Git_mode': '100644'}, 'LICENSE-Boost-1.0': {'sha256': 'c9bff75738922193e67fa726fa225535870d2aa1059f91452c411736284ad566', 'bytes': 1338, 'Git_mode': '100644'}, 'LICENSE-MIT': {'sha256': 'b2959a980bc25f5d5e020d7a31777b7184aace6eb160acc80619f85edf646f19', 'bytes': 1086, 'Git_mode': '100644'}, 'README.rst': {'sha256': 'cc22adb33eab5d154861ec8e639dc35dbf6e0878f21dfbe31c1edac8b50c2e43', 'bytes': 17708, 'Git_mode': '100644'}, 'docopt-config.cmake': {'sha256': 'd5466f48970a454ab51dc0c5c53039f1c2db089530c9cccc7af3e69d27ee2473', 'bytes': 58, 'Git_mode': '100644'}, 'docopt.cpp': {'sha256': 'ca40d5f392a51e589a6a613e79dc85e2d9e6a5eeb29588286bf01b1a9110e12d', 'bytes': 19018, 'Git_mode': '100644'}, 'docopt.h': {'sha256': 'd117f8b1a8a13f46bf2e8e69d97bfcfc877fc226c995c0f22166c26518b72727', 'bytes': 3823, 'Git_mode': '100644'}, 'docopt.pc.in': {'sha256': '58d26793ed1b29a9ecf830b084cca71376b5db5be2555a00123640f60cab1f61', 'bytes': 242, 'Git_mode': '100644'}, 'docopt_private.h': {'sha256': '82ef8330fc2019db390153964da7d56fcf8f70fb42320ab25fba323a6d5c6bc0', 'bytes': 18126, 'Git_mode': '100644'}, 'docopt_util.h': {'sha256': 'd37ce3b81986b4b799353fba286ca097f29734c56c3005c825d1b76d0ea4e7d8', 'bytes': 2670, 'Git_mode': '100644'}, 'docopt_value.h': {'sha256': 'f2a44e781828d3215a5b88b7a6519a474be31334813be87d41877266d28cbde2', 'bytes': 7175, 'Git_mode': '100644'}, 'examples/naval_fate.cpp': {'sha256': '4e57b3b2e0f3c66285cd46e207cbf7c3d17b70ebed1985edd746b1ab17bccc9c', 'bytes': 1068, 'Git_mode': '100644'}, 'main.cpp': {'sha256': '10ed142a18896d9f2d237321c62cc05c64575314de2c0a8b8597538159209d8d', 'bytes': 212, 'Git_mode': '100644'}, 'run_testcase.cpp': {'sha256': 'e5fe5fd46355850443a4ff03272936edb78189dd3226763eaaf8b89f39f03db6', 'bytes': 751, 'Git_mode': '100644'}, 'run_tests.py': {'sha256': '7c072c0a8d6a37533acefc77c4af87ab27429003b0cb286ab55aa9eacb04e894', 'bytes': 1555, 'Git_mode': '100755'}, 'testcases.docopt': {'sha256': '4237df0c9514619e8dacc4c5ec6bf71fca19de6f871d4ed6157e7adfd0b18b87', 'bytes': 11970, 'Git_mode': '100644'}}
assert len(original)==18 and not Path('.packaging-qa').exists() and not Path('.packaging-source-records').exists()
qa=Path('.packaging-qa');qa.mkdir();base=Path('.packaging-source-records');records=base/'source-notices';records.mkdir(parents=True)
for name,row in original.items():
    p=Path(name);b=p.read_bytes();assert p.is_file() and not p.is_symlink() and len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'] and bool(p.stat().st_mode&0o111)==(row['Git_mode']=='100755'),name
    q=records/(name+'.notice');q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
(records/'original-manifest.json').write_text(json.dumps(original,sort_keys=True,indent=2)+'\n')
checks=[]
for p in sorted(records.rglob('*')):
    if p.is_file():checks.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(records)))
(records/'SHA256SUMS').write_text('\n'.join(checks)+'\n')
PY_ORIGINALS
cp %{SOURCE1} .packaging-source-records/Apache-2.0.txt
cp %{PATCH0} .packaging-source-records/source-patch.patch
python3 - <<'PY_LEGAL'
import hashlib
from pathlib import Path
assert hashlib.sha256(Path('.packaging-source-records/Apache-2.0.txt').read_bytes()).hexdigest()=='cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30'
PY_LEGAL
cat > .packaging-source-records/PROVENANCE.txt <<'OWNED_PROVENANCE'
Docopt.cpp v0.6.3, exact commit 42ebcec9dc2c99a1b3a4542787572045763ad196.
Select the project's explicit BSL-1.0 whole-port offer stated in README.rst;
retain LICENSE-MIT and LICENSE-Boost-1.0, every original author notice and all
18 pre-patch source files as raw source-notices. docopt_util.h explicitly credits
boost::hash_combine for its seed-mixing helper. No particular historical Boost
version or unobserved author is invented, and no blanket MIT relicensing claim
is made. The full supplied Boost grant remains alongside the source credit.
The source snapshot is unmodified; only CMakeLists.txt and run_tests.py have the
reviewed release-stamp/Python3/full-original-test wiring changes described in
source-patch.patch. Owned packaging/consumer QA is separately Apache-2.0.
OWNED_PROVENANCE
%patch -P0 -p1
python3 - <<'PY_AFTER_PATCH'
import hashlib,json
from pathlib import Path
expected = {'.gitignore': {'sha256': '7bd15d58d4d1dcfcf4ab3d5eef5c6e7c1fda902d4ae02e6bcb5f824b63de2fa2', 'bytes': 404, 'Git_mode': '100644'}, '.travis.yml': {'sha256': 'fd4f358a5580914c47f08aeb0211b3b657298f6f551b7940554428ba1ce3d315', 'bytes': 2928, 'Git_mode': '100644'}, 'CMakeLists.txt': {'sha256': '79c84d2664c86fafd66bf67d05904294e41f1717ce04c4a765be39ca5f9e111d', 'bytes': 6622, 'Git_mode': '100644'}, 'LICENSE-Boost-1.0': {'sha256': 'c9bff75738922193e67fa726fa225535870d2aa1059f91452c411736284ad566', 'bytes': 1338, 'Git_mode': '100644'}, 'LICENSE-MIT': {'sha256': 'b2959a980bc25f5d5e020d7a31777b7184aace6eb160acc80619f85edf646f19', 'bytes': 1086, 'Git_mode': '100644'}, 'README.rst': {'sha256': 'cc22adb33eab5d154861ec8e639dc35dbf6e0878f21dfbe31c1edac8b50c2e43', 'bytes': 17708, 'Git_mode': '100644'}, 'docopt-config.cmake': {'sha256': 'd5466f48970a454ab51dc0c5c53039f1c2db089530c9cccc7af3e69d27ee2473', 'bytes': 58, 'Git_mode': '100644'}, 'docopt.cpp': {'sha256': 'ca40d5f392a51e589a6a613e79dc85e2d9e6a5eeb29588286bf01b1a9110e12d', 'bytes': 19018, 'Git_mode': '100644'}, 'docopt.h': {'sha256': 'd117f8b1a8a13f46bf2e8e69d97bfcfc877fc226c995c0f22166c26518b72727', 'bytes': 3823, 'Git_mode': '100644'}, 'docopt.pc.in': {'sha256': '58d26793ed1b29a9ecf830b084cca71376b5db5be2555a00123640f60cab1f61', 'bytes': 242, 'Git_mode': '100644'}, 'docopt_private.h': {'sha256': '82ef8330fc2019db390153964da7d56fcf8f70fb42320ab25fba323a6d5c6bc0', 'bytes': 18126, 'Git_mode': '100644'}, 'docopt_util.h': {'sha256': 'd37ce3b81986b4b799353fba286ca097f29734c56c3005c825d1b76d0ea4e7d8', 'bytes': 2670, 'Git_mode': '100644'}, 'docopt_value.h': {'sha256': 'f2a44e781828d3215a5b88b7a6519a474be31334813be87d41877266d28cbde2', 'bytes': 7175, 'Git_mode': '100644'}, 'examples/naval_fate.cpp': {'sha256': '4e57b3b2e0f3c66285cd46e207cbf7c3d17b70ebed1985edd746b1ab17bccc9c', 'bytes': 1068, 'Git_mode': '100644'}, 'main.cpp': {'sha256': '10ed142a18896d9f2d237321c62cc05c64575314de2c0a8b8597538159209d8d', 'bytes': 212, 'Git_mode': '100644'}, 'run_testcase.cpp': {'sha256': 'e5fe5fd46355850443a4ff03272936edb78189dd3226763eaaf8b89f39f03db6', 'bytes': 751, 'Git_mode': '100644'}, 'run_tests.py': {'sha256': '7ac8e1e20cf612c4f3be58670706adad6e2197f7c052cbaaab419067f4b6d9eb', 'bytes': 1564, 'Git_mode': '100755'}, 'testcases.docopt': {'sha256': '4237df0c9514619e8dacc4c5ec6bf71fca19de6f871d4ed6157e7adfd0b18b87', 'bytes': 11970, 'Git_mode': '100644'}}
assert len(expected)==18
for name,row in expected.items():
    p=Path(name);b=p.read_bytes();assert p.is_file() and not p.is_symlink() and len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'] and bool(p.stat().st_mode&0o111)==(row['Git_mode']=='100755'),name
Path('.packaging-source-records/after-manifest.json').write_text(json.dumps(expected,sort_keys=True,indent=2)+'\n')
PY_AFTER_PATCH
cat > .packaging-qa/consumer.cpp <<'OWNED_CONSUMER'
// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 openEuler RISC-V packaging contributors.
#include <docopt.h>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>
#ifdef DOCOPT_HEADER_ONLY
#error "This consumer must link the installed compiled SDK, not header-only code"
#endif
#ifdef NDEBUG
#error "Owned checks must not be compiled with NDEBUG"
#endif
static void require(bool ok) { if (!ok) throw std::runtime_error("owned check failed"); }
static void values() {
    const std::string usage = "Usage: app add <name> [--speed=<n>]\n\nOptions:\n  --speed=<n>  Speed [default: 10].\n";
    auto explicit_value = docopt::docopt_parse(usage, {"add", "Ada", "--speed=12"}, false, false);
    require(explicit_value.at("add").asBool());
    require(explicit_value.at("<name>").asString() == "Ada");
    require(explicit_value.at("--speed").asString() == "12");
    auto default_value = docopt::docopt_parse(usage, {"add", "Ada"}, false, false);
    require(default_value.at("--speed").asString() == "10");
}
static void repeated() {
    auto value = docopt::docopt_parse("Usage: app [--tag=<x>]...\n\nOptions:\n  --tag=<x>  Tag.\n", {"--tag=red", "--tag=blue"}, false, false);
    require(value.at("--tag").asStringList() == std::vector<std::string>({"red", "blue"}));
}
static void control() {
    const std::string usage = "Usage: app [-h | --version]\n\nOptions:\n  -h --help  Help.\n  --version  Version.\n";
    bool help = false, version = false;
    try { docopt::docopt_parse(usage, {"--help"}, true, false); }
    catch (const docopt::DocoptExitHelp&) { help = true; }
    try { docopt::docopt_parse(usage, {"--version"}, false, true); }
    catch (const docopt::DocoptExitVersion&) { version = true; }
    require(help && version);
}
static void bad_argv() {
    bool caught = false;
    try { docopt::docopt_parse("Usage: app <name>\n", {"--not-offered"}, false, false); }
    catch (const docopt::DocoptArgumentError&) { caught = true; }
    require(caught);
}
static void bad_usage() {
    bool caught = false;
    try { docopt::docopt_parse("No usage marker here.\n", {}, false, false); }
    catch (const docopt::DocoptLanguageError&) { caught = true; }
    require(caught);
}
static void types() {
    docopt::value truth(true), number(42), text(std::string("17"));
    docopt::value list(std::vector<std::string>({"a", "b"}));
    require(truth.isBool() && truth.asBool());
    require(number.isLong() && number.asLong() == 42);
    require(text.isString() && text.asLong() == 17);
    require(list.isStringList() && list.asStringList().size() == 2);
    docopt::value copy(list), moved(std::move(copy));
    require(moved.asStringList() == std::vector<std::string>({"a", "b"}));
    bool rejected = false;
    try { text.asBool(); } catch (const std::runtime_error&) { rejected = true; }
    require(rejected);
}
int main(int argc, char** argv) {
    try {
        require(argc == 2);
        const std::string group(argv[1]);
        if (group == "values") values();
        else if (group == "repeated") repeated();
        else if (group == "control") control();
        else if (group == "bad-argv") bad_argv();
        else if (group == "bad-usage") bad_usage();
        else if (group == "types") types();
        else throw std::runtime_error("unknown group");
        std::cout << "docopt-owned:" << group << ":PASS\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "docopt-owned:FAIL:" << error.what() << "\n";
        return 1;
    }
}
OWNED_CONSUMER
cat > .packaging-qa/CMakeLists.txt <<'OWNED_CMAKE'
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 openEuler RISC-V packaging contributors.
cmake_minimum_required(VERSION 3.20)
project(docopt_owned_consumer LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
find_package(docopt 0.6.3 EXACT CONFIG REQUIRED PATHS "${SDK_CONFIG}" NO_DEFAULT_PATH)
get_target_property(shared_type docopt TYPE)
get_target_property(static_type docopt_s TYPE)
if(NOT shared_type STREQUAL "SHARED_LIBRARY" OR NOT static_type STREQUAL "STATIC_LIBRARY")
  message(FATAL_ERROR "Both original installed imported library targets are required")
endif()
foreach(route shared static)
  add_executable(consumer-${route} consumer.cpp)
  set_target_properties(consumer-${route} PROPERTIES LINK_FLAGS "-Wl,-Map,${CMAKE_CURRENT_BINARY_DIR}/consumer-${route}.map -Wl,-t")
endforeach()
target_link_libraries(consumer-shared PRIVATE docopt)
target_link_libraries(consumer-static PRIVATE docopt_s)
file(GENERATE OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/sdk-targets.txt" CONTENT "$<TARGET_FILE:docopt>\n$<TARGET_FILE:docopt_s>\n")
OWNED_CMAKE
cat > .packaging-qa/run-qa.py <<'OWNED_RUNNER'
#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 openEuler RISC-V packaging contributors.
"""Target-only installed SDK consumers. Not a header-only/native/performance test."""
import argparse,base64,hashlib,json,os,re,shlex,stat,subprocess,sys,traceback
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--root',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
root=Path(a.root).resolve();out=Path(a.output).resolve();assert not out.exists();out.mkdir(mode=0o700);qa=root/'usr/share/docopt-cpp-tests';lib=root/'usr/lib64';config=lib/'cmake/docopt';licenses=root/'usr/share/licenses/docopt-cpp';docs=root/'usr/share/doc/docopt-cpp';groups=['values','repeated','control','bad-argv','bad-usage','types'];report={'schema_version':1,'package':'docopt-cpp','version':'0.6.3','root':str(root),'output':str(out),'commands':[],'functional_invocations':[],'status':'incomplete','header_only_claim':False,'native_ABI_or_performance_claim':False}
assert all(out!=p and p not in out.parents for p in [qa,lib,licenses,docs])
def sha(b):return hashlib.sha256(b).hexdigest()
def binary(b):return dict(bytes=len(b),sha256=sha(b),base64=base64.b64encode(b).decode())
env={k:v for k,v in os.environ.items() if k not in {'CPATH','CPLUS_INCLUDE_PATH','C_INCLUDE_PATH','LIBRARY_PATH','LD_LIBRARY_PATH','LD_PRELOAD','LD_DEBUG','CXXFLAGS','CPPFLAGS','LDFLAGS','CMAKE_PREFIX_PATH','CMAKE_MODULE_PATH','CMAKE_LIBRARY_PATH','CMAKE_INCLUDE_PATH','PKG_CONFIG_PATH','PKG_CONFIG_LIBDIR','PKG_CONFIG_SYSROOT_DIR','PYTHONPATH','PYTHONHOME'}};env.update(PATH='/usr/bin:/bin',LC_ALL='C',LANG='C',LD_LIBRARY_PATH=str(lib),PKG_CONFIG_PATH='',PKG_CONFIG_LIBDIR=str(lib/'pkgconfig'),PKG_CONFIG_SYSROOT_DIR='' if root==Path('/') else str(root))
def run(label,argv,expect=0,extra=None,timeout=300,cwd=out):
 actual=dict(env);actual.update(extra or {});p=subprocess.run([str(x) for x in argv],cwd=cwd,env=actual,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout)
 row=dict(label=label,argv=[str(x) for x in argv],cwd=str(cwd),environment={k:actual.get(k) for k in ['PATH','LC_ALL','LANG','LD_LIBRARY_PATH','LD_PRELOAD','LD_DEBUG','PKG_CONFIG_LIBDIR','PKG_CONFIG_SYSROOT_DIR','CXXFLAGS','CPPFLAGS','LDFLAGS','CMAKE_PREFIX_PATH']},exit_code=p.returncode,stdout=binary(p.stdout),stderr=binary(p.stderr));report['commands'].append(row);assert expect is None or p.returncode==expect,(label,p.returncode,p.stderr.decode(errors='replace'));return p
def manifest():
 required=[lib/'libdocopt.so.0.6.3',lib/'libdocopt.so.0',lib/'libdocopt.so',lib/'libdocopt.a',lib/'pkgconfig/docopt.pc']+[root/'usr/include/docopt'/name for name in ['docopt.h','docopt_private.h','docopt_util.h','docopt_value.h']]+list(config.rglob('*'))+list(qa.rglob('*'))+list(licenses.rglob('*'))+list(docs.rglob('*'));rows={}
 for p in sorted(set(required)):
  if p.is_dir():continue
  st=p.lstat();assert stat.S_ISREG(st.st_mode) or stat.S_ISLNK(st.st_mode);resolved=p.resolve();assert resolved.is_file();b=resolved.read_bytes();rows[str(p)]=dict(bytes=len(b),sha256=sha(b),mode=oct(st.st_mode&0o777),symlink=os.readlink(p) if p.is_symlink() else None,realpath=str(resolved))
 assert all(str(p) in rows for p in required if not p.is_dir());return rows
def same_path_in(text,target):
 for token in re.findall(r'(?:^|\s)(/[^\s()]+)',text,re.M):
  p=Path(token.strip('\'".,:;'))
  if p.exists() and os.path.samefile(p,target):return True
 return False
def elf(label,p,want_docopt):
 b=p.read_bytes();assert b[:6]==b'\x7fELF\x02\x01' and int.from_bytes(b[18:20],'little')==243,(label,'not target RISC-V ELF64 little-endian');h=run(label+'-ELF-header',['readelf','-W','-h',p]);d=run(label+'-ELF-dynamic',['readelf','-W','-d',p]);has=b'Shared library: [libdocopt.so.0]' in d.stdout
 if want_docopt is not None:assert has==want_docopt,(label,'unexpected direct docopt DSO dependency')
 return dict(path=str(p),sha256=sha(b),header=h.stdout.decode(),dynamic=d.stdout.decode(),direct_docopt_dependency=has)
try:
 assert qa.is_dir() and config.is_dir() and licenses.is_dir() and docs.is_dir()
 names=['consumer.cpp','CMakeLists.txt','run-qa.py'];checks=(qa/'SHA256SUMS').read_text().splitlines();assert len(checks)==3;expected={}
 for line in checks:
  digest,name=line.split('  ',1);assert name in names and name not in expected and re.fullmatch('[0-9a-f]{64}',digest);expected[name]=digest;assert sha((qa/name).read_bytes())==digest
 assert set(expected)==set(names) and os.path.samefile(Path(__file__),qa/'run-qa.py');report['owned_asset_hashes']=expected
 headers={'docopt.h': 'd117f8b1a8a13f46bf2e8e69d97bfcfc877fc226c995c0f22166c26518b72727', 'docopt_private.h': '82ef8330fc2019db390153964da7d56fcf8f70fb42320ab25fba323a6d5c6bc0', 'docopt_util.h': 'd37ce3b81986b4b799353fba286ca097f29734c56c3005c825d1b76d0ea4e7d8', 'docopt_value.h': 'f2a44e781828d3215a5b88b7a6519a474be31334813be87d41877266d28cbde2'}
 for name,digest in headers.items():assert sha((root/'usr/include/docopt'/name).read_bytes())==digest,(name,'original public SDK header changed')
 notice_manifest=json.loads((licenses/'source-notices/original-manifest.json').read_text());assert len(notice_manifest)==18
 for name,row in notice_manifest.items():
  p=licenses/'source-notices'/(name+'.notice');b=p.read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256']
 archive=lib/'libdocopt.a';assert archive.read_bytes().startswith(b'!<arch>\n');members=run('static-archive-member-list',['ar','t',archive]).stdout.decode().splitlines();assert members and len(members)==len(set(members)) and all(name.endswith('.o') and '/' not in name and name not in ['.','..'] for name in members);memberdir=out/'archive-members';memberdir.mkdir();report['static_archive_members']=[]
 for i,name in enumerate(members):
  p=run('static-member-bytes-'+str(i),['ar','p',archive,name]);b=p.stdout;assert b[:6]==b'\x7fELF\x02\x01' and int.from_bytes(b[16:18],'little')==1 and int.from_bytes(b[18:20],'little')==243,(name,'every archive member must be target RISC-V ELF64 relocatable');q=memberdir/(str(i)+'.o');q.write_bytes(b);h=run('static-member-ELF-header-'+str(i),['readelf','-W','-h',q]);report['static_archive_members'].append(dict(name=name,bytes=len(b),sha256=sha(b),ELF_header=h.stdout.decode()))
 assert all(os.path.samefile(p,lib/'libdocopt.so.0.6.3') for p in [lib/'libdocopt.so',lib/'libdocopt.so.0'])
 before=manifest();report['inputs_before']=before;report['DSO']=elf('production-DSO',lib/'libdocopt.so.0.6.3',None);project=out/'consumer-project';project.mkdir()
 for name in ['consumer.cpp','CMakeLists.txt']:(project/name).write_bytes((qa/name).read_bytes())
 build=out/'cmake-build';run('CMake-configure',['cmake','-S',project,'-B',build,'-DCMAKE_BUILD_TYPE=None','-DCMAKE_CXX_COMPILER=/usr/bin/g++','-DCMAKE_CXX_FLAGS=-g -UNDEBUG','-DSDK_CONFIG='+str(config),'-DCMAKE_FIND_USE_PACKAGE_REGISTRY=OFF','-DCMAKE_FIND_USE_SYSTEM_PACKAGE_REGISTRY=OFF']);built=run('CMake-build',['cmake','--build',build,'--parallel','2','--verbose'],timeout=600)
 targets=(build/'sdk-targets.txt').read_text().splitlines();assert len(targets)==2 and os.path.samefile(targets[0],lib/'libdocopt.so.0.6.3') and os.path.samefile(targets[1],lib/'libdocopt.a');report['CMake_imported_targets_same_file']=targets;report['link_proofs']={}
 binaries={'cmake-shared':build/'consumer-shared','cmake-static':build/'consumer-static'}
 for route,target in [('shared',lib/'libdocopt.so.0.6.3'),('static',lib/'libdocopt.a')]:
  mp=build/('consumer-'+route+'.map');raw=mp.read_bytes();assert same_path_in(raw.decode(),target) and same_path_in(built.stdout.decode(),target);report['link_proofs']['cmake-'+route]=dict(map=binary(raw),trace_stdout=binary(built.stdout),expected_same_file=str(target))
  # Reuse the exact compiled positive consumer object and actual generated link
  # command. Omit only its imported library; output/map paths are isolated.
  linkraw=(build/'CMakeFiles'/('consumer-'+route+'.dir')/'link.txt').read_bytes();argv=shlex.split(linkraw.decode());positions=[i for i,x in enumerate(argv) if (Path(x) if Path(x).is_absolute() else build/x).is_file() and os.path.samefile(Path(x) if Path(x).is_absolute() else build/x,target)];assert len(positions)==1
  missing=out/('cmake-no-'+route);negargv=[x for i,x in enumerate(argv) if i!=positions[0]];assert negargv.count('-o')==1;negargv[negargv.index('-o')+1]=str(missing);negargv=[('-Wl,-Map,'+str(out/('cmake-no-'+route+'.map'))) if x.startswith('-Wl,-Map,') else x for x in negargv];neg=run('cmake-'+route+'-omit-library',negargv,expect=None,cwd=build);diagnostics=neg.stdout+neg.stderr;assert neg.returncode!=0 and not missing.exists() and b'undefined reference' in diagnostics and b'docopt::docopt_parse' in diagnostics
  report['link_proofs']['cmake-'+route]['negative_control']=dict(original_link_command=binary(linkraw),only_omitted_library=argv[positions[0]],same_positive_compiled_object=True,no_output_file=True)
 assert run('pkgconf-version',['pkgconf','--modversion','docopt']).stdout==b'0.6.3\n';cflags=shlex.split(run('pkgconf-cflags',['pkgconf','--cflags','docopt']).stdout.decode());ldflags=shlex.split(run('pkgconf-libs',['pkgconf','--libs','docopt']).stdout.decode());assert ldflags.count('-ldocopt')==1 and not any(v.startswith('-l') and v!='-ldocopt' for v in ldflags)
 compiler=['g++','-std=c++11','-g','-UNDEBUG',str(qa/'consumer.cpp')]+cflags;pc=out/'consumer-pkgconfig';pcmap=out/'consumer-pkgconfig.map';positive=run('pkgconf-positive-compile-link',compiler+['-o',pc,'-Wl,-Map,'+str(pcmap),'-Wl,-t']+ldflags);assert same_path_in(positive.stdout.decode(),lib/'libdocopt.so.0.6.3') and same_path_in(pcmap.read_text(),lib/'libdocopt.so.0.6.3');report['link_proofs']['pkgconfig-shared']=dict(map=binary(pcmap.read_bytes()),trace_stdout=binary(positive.stdout),expected_same_file=str(lib/'libdocopt.so.0.6.3'));binaries['pkgconfig-shared']=pc
 negative=out/'consumer-no-library';neg=run('no-library-negative-control',compiler+['-o',negative]+[v for v in ldflags if v!='-ldocopt'],expect=None);assert neg.returncode!=0 and not negative.exists() and b'undefined reference' in neg.stderr and b'docopt::docopt_parse' in neg.stderr;report['no_library_control']=dict(only_omitted_library='-ldocopt',no_output_file=True,undefined_docopt_anchor=True)
 for route,program in binaries.items():
  report.setdefault('consumer_ELFs',{})[route]=elf(route,program,route!='cmake-static')
  for group in groups:
   p=run(route+'-'+group,[program,group]);assert p.stdout==('docopt-owned:'+group+':PASS\n').encode() and p.stderr==b'';report['functional_invocations'].append(dict(route=route,group=group,program=str(program)))
  if route!='cmake-static':
   p=run(route+'-loaded-DSO-trace',[program,'values'],extra={'LD_DEBUG':'libs,files'});assert p.stdout==b'docopt-owned:values:PASS\n' and same_path_in(p.stderr.decode(),lib/'libdocopt.so.0.6.3');report.setdefault('loaded_DSO_same_file',{})[route]=dict(expected=str(lib/'libdocopt.so.0.6.3'),raw_trace=binary(p.stderr))
 assert len(report['functional_invocations'])==18;after=manifest();assert after==before;report.update(status='passed',semantic_groups=6,API_routes=3,functional_invocations_count=18,loader_trace_probes=2,input_manifest_unchanged=True,inputs_after=after,all_owned_assets_verified_again=all(sha((qa/name).read_bytes())==digest for name,digest in expected.items()));assert report['all_owned_assets_verified_again']
except BaseException as error:report.update(status='failed',error=repr(error),traceback=traceback.format_exc());raise
finally:
 text=json.dumps(report,sort_keys=True,indent=2);(out/'receipt.json').write_text(text+'\n');print('BEGIN_DOCOPT_OWNED_QA_JSON');print(text);print('END_DOCOPT_OWNED_QA_JSON')
OWNED_RUNNER
chmod 0644 .packaging-qa/consumer.cpp .packaging-qa/CMakeLists.txt .packaging-qa/run-qa.py
(cd .packaging-qa && sha256sum consumer.cpp CMakeLists.txt run-qa.py > SHA256SUMS)

%build
export LC_ALL=C LANG=C
export CXXFLAGS="%{optflags} -g -UNDEBUG"
export LDFLAGS="%{?build_ldflags}"
cmake -S . -B build -DCMAKE_BUILD_TYPE=None -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_LIBDIR=%{_lib} -DWITH_TESTS=ON
cmake --build build --parallel 2 --verbose

%install
DESTDIR=%{buildroot} cmake --install build
install -d %{buildroot}%{_datadir}/docopt-cpp-tests %{buildroot}%{_licensedir}/%{name} %{buildroot}%{_docdir}/%{name}
install -m0644 .packaging-qa/consumer.cpp .packaging-qa/CMakeLists.txt .packaging-qa/run-qa.py .packaging-qa/SHA256SUMS %{buildroot}%{_datadir}/docopt-cpp-tests/
install -m0644 LICENSE-MIT LICENSE-Boost-1.0 .packaging-source-records/Apache-2.0.txt %{buildroot}%{_licensedir}/%{name}/
cp -a .packaging-source-records/source-notices %{buildroot}%{_licensedir}/%{name}/
install -m0644 README.rst .packaging-source-records/PROVENANCE.txt .packaging-source-records/source-patch.patch %{buildroot}%{_docdir}/%{name}/

%check
export LC_ALL=C LANG=C
python3 - <<'PY_CHECK_SOURCE'
import hashlib,json
from pathlib import Path
expected=json.loads(Path('.packaging-source-records/after-manifest.json').read_text());original=json.loads(Path('.packaging-source-records/source-notices/original-manifest.json').read_text());assert len(expected)==len(original)==18
for name,row in expected.items():
    p=Path(name);b=p.read_bytes();assert p.is_file() and not p.is_symlink() and len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'] and bool(p.stat().st_mode&0o111)==(row['Git_mode']=='100755'),name
    notice=Path('.packaging-source-records/source-notices')/(name+'.notice');old=original[name];assert len(notice.read_bytes())==old['bytes'] and hashlib.sha256(notice.read_bytes()).hexdigest()==old['sha256']
PY_CHECK_SOURCE
ctest --test-dir build --show-only=json-v1 > .packaging-qa/original-test-registry.json
set +e
ctest --test-dir build --verbose --output-on-failure --timeout 600 > .packaging-qa/original-tests.log 2>&1
original_status=$?
set -e
cat .packaging-qa/original-tests.log
test "$original_status" -eq 0
python3 - <<'PY_ORIGINAL_TESTS'
import base64,hashlib,json,re
from pathlib import Path
registry=json.loads(Path('.packaging-qa/original-test-registry.json').read_text());assert len(registry['tests'])==1 and registry['tests'][0]['name']=='docopt-testcases'
raw=Path('.packaging-qa/original-tests.log').read_bytes();text=raw.decode();assert len(re.findall(r'(?m)^(?:[0-9]+: )?PASS \(175\)\s*$',text))==1 and '100%% tests passed, 0 tests failed out of 1' in text
fixture=Path('testcases.docopt').read_bytes();assert hashlib.sha256(fixture).hexdigest()=='4237df0c9514619e8dacc4c5ec6bf71fca19de6f871d4ed6157e7adfd0b18b87'
print('DOCOPT_ORIGINAL_175_TESTS '+json.dumps(dict(registry=registry,fixture_sha256=hashlib.sha256(fixture).hexdigest(),raw_log=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),base64=base64.b64encode(raw).decode())),sort_keys=True))
PY_ORIGINAL_TESTS
(cd %{buildroot}%{_datadir}/docopt-cpp-tests && sha256sum -c SHA256SUMS)
python3 %{buildroot}%{_datadir}/docopt-cpp-tests/run-qa.py --root %{buildroot} --output "$PWD/.packaging-qa/build-qa-results"

%files
%{_libdir}/libdocopt.so.0.6.3
%{_libdir}/libdocopt.so.0
%{_libdir}/libdocopt.so
%{_libdir}/libdocopt.a
%{_includedir}/docopt
%{_libdir}/pkgconfig/docopt.pc
%{_libdir}/cmake/docopt
%{_datadir}/docopt-cpp-tests
%license %{_licensedir}/%{name}
%doc %{_docdir}/%{name}

%changelog
* Wed Oct 28 2026 yinjiayi - 0.6.3-1
- Preserve the original shared/static SDK and full opt-in 175-case workload.
- Correct release/test metadata and add closed installed SDK consumer checks.
