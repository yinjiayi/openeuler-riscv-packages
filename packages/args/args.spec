# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 openEuler package contributors.
# Header-only production SDK: no installed ELF to strip into debuginfo.
%global debug_package %{nil}
Name:           args
Version:        6.6.1
Release:        1%{?dist}
Summary:        Header-only C++11 command-line argument parsing library
License:        MIT AND Unlicense AND Apache-2.0
URL:            https://github.com/Taywee/args
Source0:        args-%{version}.tar.gz
Source1:        Apache-2.0.txt

BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  cmake >= 3.14
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  gcc-c++
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  gzip
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  python3
BuildRequires:  tar
Requires:       bash
Requires:       binutils
Requires:       cmake >= 3.14
Requires:       coreutils
Requires:       gcc-c++
Requires:       glibc-devel
Requires:       make
Requires:       pkgconf-pkg-config
Requires:       python3

%description
A single-header C++11 argument parsing SDK. The documented CMake route
preserves both default examples, all original tests and upstream hardening.
This single package installs the original header, CMake exports and pkg-config
metadata, plus additive target-only installed SDK checks.

%prep
%setup -q -n Taywee-args-3541420
python3 - <<'PY_SNAPSHOT'
import hashlib,json,pathlib,shutil
root=pathlib.Path('.')
assert not (root/'.packaging-qa').exists() and not (root/'.packaging-build').exists()
files=sorted(p for p in root.rglob('*') if p.is_file())
assert len(files)==209 and all(not p.is_symlink() for p in files)
q=root/'.packaging-qa';q.mkdir()
manifest={}
for p in files:
    b=p.read_bytes();name=p.as_posix()
    manifest[name]={'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'mode':p.stat().st_mode&0o777}
    dest=q/'source-notices'/(name+'.notice');dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
(q/'original-manifest.json').write_text(json.dumps(manifest,sort_keys=True)+'\n')
(q/'source-notices/SHA256SUMS').write_text(''.join(v['sha256']+'  '+p+'.notice\n' for p,v in sorted(manifest.items())))
assert manifest['args.hxx']['sha256']=='de5cd83556938cc022ceaf61282423cf5c546b612d2d1e866d1b5507e2c53d2d'
assert manifest['LICENSE']['sha256']=='e434153d0eab720e3a4d2b6f7721e4168d6cade2ac940984705a6506208c1444'
license=pathlib.Path('%{SOURCE1}').read_bytes()
assert hashlib.sha256(license).hexdigest()=='cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30'
(q/'Apache-2.0.txt').write_bytes(license)
PY_SNAPSHOT
cat > .packaging-qa/consumer.cpp <<'ARGS_QA_CONSUMER_CPP'
/* Copyright 2026 openEuler package contributors.
 * SPDX-License-Identifier: Apache-2.0
 * The complete Apache-2.0 grant is installed with this owned QA source.
 */
#include <args.hxx>
#include <cstdio>
#include <cstring>
#include <sstream>
#include <string>
#include <vector>
#ifdef NDEBUG
#error Owned checks must remain active
#endif
#define CHECK(v) do { if (!(v)) { std::fprintf(stderr, "check failed at line %%d: %%s\n", __LINE__, #v); return 1; } } while (0)
static_assert(ARGS_VERSION_MAJOR == 6 && ARGS_VERSION_MINOR == 6 && ARGS_VERSION_PATCH == 1,
              "The installed SDK must be the selected release");
int main()
{
    CHECK(std::strcmp(ARGS_VERSION, "6.6.1") == 0);
    std::puts("PASS 1 selected public version");
    {
        args::ArgumentParser parser("owned parser");
        args::Flag verbose(parser, "verbose", "verbose mode", {'v', "verbose"});
        args::ValueFlag<int> count(parser, "COUNT", "count", {'n', "count"});
        args::Positional<std::string> input(parser, "INPUT", "input");
        parser.ParseArgs(std::vector<std::string>{"-v", "--count", "7", "input.dat"});
        CHECK(args::get(verbose) && args::get(count) == 7 && args::get(input) == "input.dat");
    }
    std::puts("PASS 2 flags and positional values");
    {
        args::ArgumentParser parser("owned list");
        args::ValueFlagList<int> numbers(parser, "NUMBER", "numbers", {'n', "number"});
        parser.ParseArgs(std::vector<std::string>{"--number", "1", "--number", "2", "--number", "3"});
        CHECK(args::get(numbers) == std::vector<int>({1, 2, 3}));
    }
    std::puts("PASS 3 repeated values preserve order");
    {
        args::ArgumentParser parser("owned mapping");
        args::MapFlag<std::string, int> color(parser, "COLOR", "color", {'c', "color"}, {{"red", 1}, {"blue", 2}});
        parser.ParseArgs(std::vector<std::string>{"--color", "blue"});
        CHECK(args::get(color) == 2);
    }
    std::puts("PASS 4 mapped public value");
    {
        bool bad_number = false, unknown_flag = false;
        try {
            args::ArgumentParser parser("owned invalid number");
            args::ValueFlag<int> count(parser, "COUNT", "count", {'n', "count"});
            parser.ParseArgs(std::vector<std::string>{"--count", "12x"});
        } catch (const args::ParseError &) { bad_number = true; }
        try {
            args::ArgumentParser parser("owned unknown flag");
            parser.ParseArgs(std::vector<std::string>{"--does-not-exist"});
        } catch (const args::ParseError &) { unknown_flag = true; }
        CHECK(bad_number && unknown_flag);
    }
    std::puts("PASS 5 malformed inputs raise ParseError");
    {
        args::ArgumentParser parser("owned help description");
        args::HelpFlag help(parser, "help", "display owned help", {'h', "help"});
        bool caught = false;
        try { parser.ParseArgs(std::vector<std::string>{"--help"}); }
        catch (const args::Help &) { caught = true; }
        std::ostringstream rendered; rendered << parser;
        CHECK(caught && rendered.str().find("owned help description") != std::string::npos
              && rendered.str().find("--help") != std::string::npos);
    }
    std::puts("PASS 6 help exception and rendering");
    return 0;
}
ARGS_QA_CONSUMER_CPP
cat > .packaging-qa/CMakeLists.txt <<'ARGS_QA_CMAKELISTS_TXT'
# Copyright 2026 openEuler package contributors.
# SPDX-License-Identifier: Apache-2.0
cmake_minimum_required(VERSION 3.14)
project(args_owned_consumer LANGUAGES CXX)
if(NOT DEFINED QA_PREFIX)
  message(FATAL_ERROR "QA_PREFIX is required")
endif()
if(QA_WRONG_VERSION)
  set(QA_VERSION 6.6.2)
else()
  set(QA_VERSION 6.6.1)
endif()
find_package(args ${QA_VERSION} EXACT CONFIG REQUIRED
  PATHS "${QA_PREFIX}/share/cmake/args" NO_DEFAULT_PATH)
if(NOT TARGET taywee::args)
  message(FATAL_ERROR "Original exported target is required")
endif()
file(GENERATE OUTPUT "${CMAKE_BINARY_DIR}/export-usage.txt" CONTENT
  "includes=$<TARGET_PROPERTY:taywee::args,INTERFACE_INCLUDE_DIRECTORIES>\nfeatures=$<TARGET_PROPERTY:taywee::args,INTERFACE_COMPILE_FEATURES>\ndefinitions=$<TARGET_PROPERTY:taywee::args,INTERFACE_COMPILE_DEFINITIONS>\n")
add_executable(args-consumer consumer.cpp)
set_target_properties(args-consumer PROPERTIES CXX_STANDARD 11 CXX_STANDARD_REQUIRED YES)
target_compile_options(args-consumer PRIVATE -Wall -Wextra -Werror -MD)
target_link_libraries(args-consumer PRIVATE taywee::args)
ARGS_QA_CMAKELISTS_TXT
cat > .packaging-qa/expected.stdout <<'ARGS_QA_EXPECTED_STDOUT'
PASS 1 selected public version
PASS 2 flags and positional values
PASS 3 repeated values preserve order
PASS 4 mapped public value
PASS 5 malformed inputs raise ParseError
PASS 6 help exception and rendering
ARGS_QA_EXPECTED_STDOUT
cat > .packaging-qa/run-qa.py <<'ARGS_QA_RUN_QA_PY'
#!/usr/bin/env python3
# Copyright 2026 openEuler package contributors.
# SPDX-License-Identifier: Apache-2.0
"""Target-only installed/staged header SDK check, not a library/source build.
Never run this helper on the local review host. Raw evidence is retained.
"""
import argparse,base64,hashlib,json,os,shlex,shutil,subprocess,tempfile
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--prefix',required=True);a=ap.parse_args()
prefix=Path(a.prefix).resolve();qa=prefix/'share/args-tests';header=prefix/'include/args.hxx';sdk=[header,prefix/'share/cmake/args/args-config.cmake',prefix/'share/cmake/args/args-config-version.cmake',prefix/'share/pkgconfig/args.pc'];assets=[qa/v for v in ['consumer.cpp','CMakeLists.txt','expected.stdout','run-qa.py','SHA256SUMS']]
def sha(b):return hashlib.sha256(b).hexdigest()
def snapshot(paths):
 rows={}
 for p in paths:
  assert p.is_file() and not p.is_symlink();b=p.read_bytes();rows[str(p)]=dict(sha256=sha(b),bytes=len(b),realpath=str(p.resolve()))
 return rows
before=snapshot(sdk+assets);assert Path(__file__).resolve().samefile(qa/'run-qa.py')
expected=(qa/'expected.stdout').read_bytes();assert expected.count(b'PASS ')==6
for line in (qa/'SHA256SUMS').read_text().splitlines():
 digest,name=line.split('  ',1);assert name in {'consumer.cpp','CMakeLists.txt','expected.stdout','run-qa.py'} and sha((qa/name).read_bytes())==digest
assert header.read_bytes()==(prefix/'share/licenses/args/source-notices/args.hxx.notice').read_bytes()
work=Path(tempfile.mkdtemp(prefix='args-owned-'));source=work/'source';source.mkdir();records=[];chunks={}
for name in ['consumer.cpp','CMakeLists.txt']:shutil.copyfile(qa/name,source/name)
env=os.environ.copy()
for name in ['LD_LIBRARY_PATH','LIBRARY_PATH','CPATH','CPLUS_INCLUDE_PATH','C_INCLUDE_PATH','CMAKE_PREFIX_PATH','CXXFLAGS','CPPFLAGS','LDFLAGS','PKG_CONFIG_PATH','PKG_CONFIG_LIBDIR','PKG_CONFIG_SYSROOT_DIR']:env.pop(name,None)
env.update(LC_ALL='C',LANG='C',CXX='g++',CXXFLAGS='-O2 -g',PKG_CONFIG_PATH=str(prefix/'share/pkgconfig'),PKG_CONFIG_LIBDIR=str(prefix/'share/pkgconfig'),PKG_CONFIG_ALLOW_SYSTEM_CFLAGS='1')
def remember(name,b):chunks[name]=dict(sha256=sha(b),bytes=len(b),base64=base64.b64encode(b).decode());(work/name).write_bytes(b)
def run(label,argv,want=0,timeout=120):
 try:
  p=subprocess.run(argv,cwd=work,env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout);code,out,err,timed_out=p.returncode,p.stdout,p.stderr,False
 except subprocess.TimeoutExpired as error:
  code,out,err,timed_out=None,error.stdout or b'',error.stderr or b'',True
 remember(label+'.stdout',out);remember(label+'.stderr',err)
 row=dict(label=label,argv=argv,cwd=str(work),exit=code,timed_out=timed_out,timeout_seconds=timeout,stdout_sha256=sha(out),stderr_sha256=sha(err),relevant_environment={k:env[k] for k in ['LC_ALL','LANG','CXX','CXXFLAGS','PKG_CONFIG_PATH','PKG_CONFIG_LIBDIR','PKG_CONFIG_ALLOW_SYSTEM_CFLAGS']});records.append(row)
 print('ARGS_OWNED_QA_COMMAND '+json.dumps(row,sort_keys=True),flush=True)
 print('ARGS_OWNED_QA_RAW '+json.dumps({label+'.'+kind:chunks[label+'.'+kind] for kind in ['stdout','stderr']},sort_keys=True),flush=True)
 assert not timed_out,('command timeout',label)
 assert (code==want) if want is not None else code!=0
 return subprocess.CompletedProcess(argv,code,out,err)
print('ARGS_OWNED_QA_CONTEXT '+json.dumps(dict(prefix=str(prefix),work=str(work),source=str(source),helper_sha256=before[str(qa/'run-qa.py')]['sha256'],selected_SDK_QA_before=before),sort_keys=True),flush=True)
run('compiler-version',['g++','--version']);run('cmake-version',['cmake','--version']);pc=run('pkgconfig-version',['pkg-config','--modversion','args']);assert pc.stdout==b'6.6.1\n' and pc.stderr==b''
pcflags=run('pkgconfig-cflags',['pkg-config','--define-variable=prefix='+str(prefix),'--cflags','args']);assert pcflags.stderr==b'';flags=shlex.split(pcflags.stdout.decode());assert flags==['-I'+str(prefix/'include')]
positive=work/'positive';run('positive-configure',['cmake','-S',str(source),'-B',str(positive),'-G','Unix Makefiles','-DQA_PREFIX='+str(prefix),'-DCMAKE_CXX_COMPILER=g++']);run('positive-build',['cmake','--build',str(positive),'--verbose'],timeout=180)
exe=positive/'args-consumer';assert exe.is_file();exe_before=sha(exe.read_bytes());program=run('six-public-groups',[str(exe)],timeout=30);assert program.stdout==expected and program.stderr==b'' and sha(exe.read_bytes())==exe_before
dependencies=list(positive.rglob('consumer.cpp.o.d'));assert len(dependencies)==1;dep=dependencies[0].read_bytes();remember('consumer.dependencies',dep);words=shlex.split(dep.decode().replace('\\\n',' '));same=[v for v in words if Path(v).is_file() and os.path.samefile(v,header)];assert same and len(set(same))==1
usage=(positive/'export-usage.txt').read_bytes();remember('export-usage.txt',usage);assert str(prefix/'include').encode() in usage
elf=run('consumer-readelf',['readelf','-h',str(exe)]);assert b'ELF64' in elf.stdout and b'RISC-V' in elf.stdout
negative=work/'negative';rejected=run('wrong-exact-version',['cmake','-S',str(source),'-B',str(negative),'-G','Unix Makefiles','-DQA_PREFIX='+str(prefix),'-DQA_WRONG_VERSION=ON','-DCMAKE_CXX_COMPILER=g++'],want=None)
assert not (negative/'args-consumer').exists() and b'6.6.2' in rejected.stdout+rejected.stderr and b'6.6.1' in rejected.stdout+rejected.stderr and b'args-config.cmake' in rejected.stdout+rejected.stderr
after=snapshot(sdk+assets);assert before==after
evidence=dict(prefix=str(prefix),work=str(work),source=str(source),helper_sha256=before[str(qa/'run-qa.py')]['sha256'],all_four_installed_SDK_files_before={str(p):before[str(p)] for p in sdk},owned_QA_files_before={str(p):before[str(p)] for p in assets},all_selected_SDK_QA_bytes_unchanged=True,public_groups=6,program_sha256_before=exe_before,program_sha256_after=sha(exe.read_bytes()),installed_same_file_header_paths=same,stock_exported_target='taywee::args',pkgconfig_version='6.6.1',negative_control='Wrong exact SDK version rejected at configure, not an omitted archive or native loader test',commands=records,raw_chunks=chunks,target_execution=True,no_library_or_original_source_build=True,no_native_or_performance_claim=True)
(work/'evidence.json').write_text(json.dumps(evidence,sort_keys=True)+'\n');print('ARGS_OWNED_QA_EVIDENCE_BEGIN');print(json.dumps(evidence,sort_keys=True));print('ARGS_OWNED_QA_EVIDENCE_END')
ARGS_QA_RUN_QA_PY

chmod 0755 .packaging-qa/run-qa.py

%build
export CXXFLAGS="%{optflags}"
export LDFLAGS="%{?build_ldflags}"
cmake -S . -B .packaging-build -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_LIBDIR=%{_lib} -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
cmake --build .packaging-build --parallel 2

%install
DESTDIR=%{buildroot} cmake --install .packaging-build
install -d %{buildroot}%{_datadir}/args-tests %{buildroot}%{_licensedir}/args
install -m 0644 .packaging-qa/consumer.cpp .packaging-qa/CMakeLists.txt .packaging-qa/expected.stdout %{buildroot}%{_datadir}/args-tests/
install -m 0755 .packaging-qa/run-qa.py %{buildroot}%{_datadir}/args-tests/
python3 - <<'PY_INSTALL'
import hashlib,pathlib,shutil
qa=pathlib.Path('%{buildroot}%{_datadir}/args-tests')
names=['consumer.cpp','CMakeLists.txt','expected.stdout','run-qa.py']
(qa/'SHA256SUMS').write_text(''.join(hashlib.sha256((qa/name).read_bytes()).hexdigest()+'  '+name+'\n' for name in names))
licenses=pathlib.Path('%{buildroot}%{_licensedir}/args')
shutil.copyfile('LICENSE',licenses/'LICENSE.MIT')
shutil.copyfile('.packaging-qa/Apache-2.0.txt',licenses/'Apache-2.0.txt')
shutil.copytree('.packaging-qa/source-notices',licenses/'source-notices')
PY_INSTALL

%check
export LC_ALL=C LANG=C
python3 - <<'PY_BEFORE'
import hashlib,json,pathlib
m=json.loads(pathlib.Path('.packaging-qa/original-manifest.json').read_text());assert len(m)==209
for p,v in m.items():
    f=pathlib.Path(p);b=f.read_bytes();assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256'] and f.stat().st_mode&0o777==v['mode']
commands=json.loads(pathlib.Path('.packaging-build/compile_commands.json').read_text())
root=pathlib.Path('.').resolve();actual={}
for row in commands:
    p=pathlib.Path(row['file']).resolve().relative_to(root).as_posix()
    assert p not in actual;actual[p]=row
expected={p for p in m if p.startswith('test/') and p.endswith('.cxx')}|{'examples/gitlike.cxx','examples/completion.cxx'}
assert len(expected)==99 and set(actual)==expected
for p,row in actual.items():
    command=row.get('command',' '.join(row.get('arguments',[])))
    if p.startswith('test/'):assert '-Werror' in command
assert '-fno-exceptions' in actual['test/no_exceptions.cxx'].get('command',' '.join(actual['test/no_exceptions.cxx'].get('arguments',[])))
assert pathlib.Path('.packaging-build/gitlike').is_file() and pathlib.Path('.packaging-build/completion').is_file()
print('ARGS_DEFAULT_BUILD_99_TRANSLATION_UNITS_2_EXAMPLES_NO_EXCEPTIONS_RETAINED')
PY_BEFORE
ctest --test-dir .packaging-build --show-only=json-v1 > .packaging-qa/ctest-registered.json
set +e
ctest --test-dir .packaging-build -V --output-on-failure > .packaging-qa/ctest.stdout 2> .packaging-qa/ctest.stderr
ctest_status=$?
set -e
export ARGS_CTEST_RC="$ctest_status"
python3 - <<'PY_CTEST'
import json,os,pathlib,re,sys
q=pathlib.Path('.packaging-qa')
stdout=(q/'ctest.stdout').read_bytes();stderr=(q/'ctest.stderr').read_bytes()
sys.stdout.buffer.write(stdout);sys.stderr.buffer.write(stderr)
original=json.loads((q/'original-manifest.json').read_text())
names=sorted(pathlib.PurePosixPath(p).stem for p in original if re.fullmatch(r'test/[^/]+[.]cxx',p) and not re.search(r'[.]aux[^/]*[.]cxx$',p))
listing=json.loads((q/'ctest-registered.json').read_text());registered=[v['name'] for v in listing['tests']]
assert len(names)==len(registered)==96 and sorted(registered)==names
assert os.environ['ARGS_CTEST_RC']=='0' and b'100%% tests passed, 0 tests failed out of 96' in stdout
assert len(re.findall(rb'Test\s+#\d+:.*?\sPassed\s',stdout))==96
assert not re.search(rb'\*\*\*(?:Not Run|Skipped|Failed)',stdout+stderr)
print('ARGS_ORIGINAL_UNFILTERED_CTEST_96_INVOCATIONS_PASSED')
PY_CTEST
python3 %{buildroot}%{_datadir}/args-tests/run-qa.py --prefix %{buildroot}%{_prefix}
python3 - <<'PY_AFTER'
import hashlib,json,pathlib
m=json.loads(pathlib.Path('.packaging-qa/original-manifest.json').read_text());assert len(m)==209
for p,v in m.items():
    f=pathlib.Path(p);b=f.read_bytes();assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256'] and f.stat().st_mode&0o777==v['mode']
print('ARGS_ALL_209_ORIGINAL_SOURCE_FILES_UNCHANGED')
PY_AFTER

%files
%license %{_licensedir}/args
%doc README.md
%{_includedir}/args.hxx
%{_datadir}/cmake/args/args-config.cmake
%{_datadir}/cmake/args/args-config-version.cmake
%{_datadir}/pkgconfig/args.pc
%{_datadir}/args-tests/

%changelog
* Wed Oct 28 2026 openEuler package contributors - 6.6.1-1
- Preserve the original CMake defaults and add installed header SDK checks.
