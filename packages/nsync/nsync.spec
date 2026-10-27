# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 openEuler package contributors.
Name:           nsync
Version:        1.30.0
Release:        1%{?dist}
Summary:        Portable synchronization primitives for C and C++
License:        Apache-2.0
URL:            https://github.com/google/nsync
# Local source-cache basename; the observed publisher URL is in sources.yaml.
Source0:        nsync-%{version}.tar.gz
Patch0:         0001-export-Cpp-ABI-definitions.patch

BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  cmake >= 3.14
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  gzip
BuildRequires:  make
BuildRequires:  patch
BuildRequires:  python3
BuildRequires:  tar
Requires:       bash
Requires:       binutils
Requires:       cmake >= 3.14
Requires:       coreutils
Requires:       gcc
Requires:       gcc-c++
Requires:       glibc-devel
Requires:       make
Requires:       python3

%description
Portable userspace locks, condition variables, run-once initialization,
waitable counters and notification notes. This single SDK package preserves
the documented CMake route's default C and C++ static libraries and headers.

%prep
%setup -q -n google-nsync-55155ca
# Only fresh downstream directories may receive packaging writes.
python3 - <<'PY_SNAPSHOT'
import hashlib,json,pathlib,shutil
root=pathlib.Path('.')
assert not (root/'.packaging-qa').exists() and not (root/'.packaging-build').exists()
original=sorted(p for p in root.rglob('*') if p.is_file())
assert len(original)==315 and all(not p.is_symlink() for p in original)
q=root/'.packaging-qa';q.mkdir()
manifest={}
for p in original:
    b=p.read_bytes();name=p.as_posix()
    manifest[name]={'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'mode':p.stat().st_mode&0o777}
    destination=q/'source-notices'/(name+'.notice')
    destination.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(p,destination)
(q/'original-manifest.json').write_text(json.dumps(manifest,sort_keys=True)+'\n')
(q/'source-notices/SHA256SUMS').write_text(''.join(v['sha256']+'  '+p+'.notice\n' for p,v in sorted(manifest.items())))
shutil.copyfile('LICENSE',q/'LICENSE.original')
PY_SNAPSHOT
%autopatch -p1
python3 - <<'PY_PATCHED'
import hashlib,json,pathlib
q=pathlib.Path('.packaging-qa')
original=json.loads((q/'original-manifest.json').read_text())
assert len(original)==315 and original['CMakeLists.txt']['sha256']=='10c97ffffbcd570e3c7c86a90a6442b838d59fa04242e2210a25b463f32aea76'
expected={p:dict(v) for p,v in original.items()}
expected['CMakeLists.txt'].update(sha256='8ced83088589b9796a4015b9b3e466b86291d7de115fed06e1d7929901e2565c',bytes=13748)
assert [p for p in original if original[p]!=expected[p]]==['CMakeLists.txt']
for p,v in expected.items():
    f=pathlib.Path(p);b=f.read_bytes();assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256'] and f.stat().st_mode&0o777==v['mode']
(q/'patched-source-manifest.json').write_text(json.dumps(expected,sort_keys=True)+'\n')
print('NSYNC_PATCH_PROOF '+json.dumps({'original_files':315,'unchanged_files':314,'changed_file':'CMakeLists.txt','before_sha256':'10c97ffffbcd570e3c7c86a90a6442b838d59fa04242e2210a25b463f32aea76','after_sha256':'8ced83088589b9796a4015b9b3e466b86291d7de115fed06e1d7929901e2565c'},sort_keys=True))
PY_PATCHED
find public -type f -name '*.h' -print | LC_ALL=C sort > .packaging-qa/header-paths
cat > .packaging-qa/consumer.c <<'NSYNC_QA_CONSUMER_C'
/* Copyright 2026 openEuler package contributors.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy at http://www.apache.org/licenses/LICENSE-2.0 .
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#include <stdio.h>
#include <nsync.h>
NSYNC_CPP_USING_
#ifdef __cplusplus
#include <atomic>
#include <type_traits>
static_assert(std::is_same<nsync_once, std::atomic<uint32_t> >::value,
              "Imported C++ target must expose its public once type");
#endif

#ifdef NDEBUG
#error Owned API checks must not be compiled with NDEBUG
#endif
#define CHECK(v) do { if (!(v)) { fprintf(stderr, "check failed at line %%d: %%s\n", __LINE__, #v); return 1; } } while (0)
static void add_one(void *arg) { ++*(int *)arg; }

int main(void) {
    nsync_mu mu = NSYNC_MU_INIT;
    nsync_once once = NSYNC_ONCE_INIT;
    int calls = 0;
    nsync_counter counter;
    nsync_note parent, child;
    struct nsync_waitable_s objects[2];
    struct nsync_waitable_s *waitables[2] = { &objects[0], &objects[1] };

    nsync_mu_lock(&mu);
    nsync_mu_assert_held(&mu);
    CHECK(!nsync_mu_is_reader(&mu));
    nsync_mu_unlock(&mu);
    nsync_mu_rlock(&mu);
    nsync_mu_rassert_held(&mu);
    CHECK(nsync_mu_is_reader(&mu));
    nsync_mu_runlock(&mu);
    puts("PASS 1 mutex writer and reader modes");

    nsync_run_once_arg(&once, add_one, &calls);
    nsync_run_once_arg(&once, add_one, &calls);
    CHECK(calls == 1);
    puts("PASS 2 once executes one initializer");

    counter = nsync_counter_new(2);
    CHECK(counter != NULL);
    CHECK(nsync_counter_value(counter) == 2);
    CHECK(nsync_counter_add(counter, -1) == 1);
    CHECK(nsync_counter_add(counter, -1) == 0);
    CHECK(nsync_counter_wait(counter, nsync_time_zero) == 0);
    nsync_counter_free(counter);
    puts("PASS 3 counter reaches zero without delayed wait");

    parent = nsync_note_new(NULL, nsync_time_no_deadline);
    CHECK(parent != NULL);
    child = nsync_note_new(parent, nsync_time_no_deadline);
    CHECK(child != NULL);
    CHECK(!nsync_note_is_notified(parent) && !nsync_note_is_notified(child));
    nsync_note_notify(parent);
    CHECK(nsync_note_is_notified(parent) && nsync_note_is_notified(child));
    CHECK(nsync_note_wait(child, nsync_time_zero));
    nsync_note_free(child);
    nsync_note_free(parent);
    puts("PASS 4 note notification propagates to child");

    CHECK(nsync_time_cmp(nsync_time_ms(1500), nsync_time_s_ns(1, 500000000)) == 0);
    CHECK(nsync_time_cmp(nsync_time_add(nsync_time_ms(1000), nsync_time_us(500000)), nsync_time_ms(1500)) == 0);
    CHECK(nsync_time_cmp(nsync_time_sub(nsync_time_ms(1500), nsync_time_ms(1000)), nsync_time_ms(500)) == 0);
    CHECK(nsync_time_cmp(nsync_time_ms(1), nsync_time_zero) > 0);
    puts("PASS 5 time arithmetic has exact unit conversions");

    parent = nsync_note_new(NULL, nsync_time_no_deadline);
    counter = nsync_counter_new(0);
    CHECK(parent != NULL && counter != NULL);
    objects[0].v = parent;
    objects[0].funcs = &nsync_note_waitable_funcs;
    objects[1].v = counter;
    objects[1].funcs = &nsync_counter_waitable_funcs;
    CHECK(nsync_wait_n(NULL, NULL, NULL, nsync_time_zero, 2, waitables) == 1);
    nsync_counter_free(counter);
    nsync_note_free(parent);
    puts("PASS 6 wait selects an already ready counter");
    return 0;
}
NSYNC_QA_CONSUMER_C
cat > .packaging-qa/CMakeLists.txt <<'NSYNC_QA_CMAKELISTS_TXT'
# SPDX-License-Identifier: Apache-2.0
cmake_minimum_required(VERSION 3.14)
project(nsync_owned_consumer LANGUAGES C CXX)
if(NOT DEFINED QA_PREFIX OR NOT DEFINED QA_PROFILE OR NOT DEFINED QA_MAP)
  message(FATAL_ERROR "QA_PREFIX, QA_PROFILE and QA_MAP are required")
endif()
if(QA_PROFILE STREQUAL "c")
  find_package(nsync CONFIG REQUIRED PATHS "${QA_PREFIX}/lib64/cmake/nsync" NO_DEFAULT_PATH)
  set(QA_LIBRARY nsync)
elseif(QA_PROFILE STREQUAL "cpp")
  find_package(nsync_cpp CONFIG REQUIRED PATHS "${QA_PREFIX}/lib64/cmake/nsync_cpp" NO_DEFAULT_PATH)
  set(QA_LIBRARY nsync_cpp)
  set_source_files_properties(consumer.c PROPERTIES LANGUAGE CXX)
else()
  message(FATAL_ERROR "Unknown profile")
endif()
add_executable(nsync-consumer consumer.c)
target_compile_options(nsync-consumer PRIVATE -Wall -Wextra -Werror -UNDEBUG -pthread)
target_link_options(nsync-consumer PRIVATE -pthread "-Wl,-t,-Map,${QA_MAP}")
if(QA_PROFILE STREQUAL "c")
  target_compile_features(nsync-consumer PRIVATE c_std_11)
else()
  target_compile_features(nsync-consumer PRIVATE cxx_std_11)
endif()
# Staged %%check cannot use the host's /usr/include as its staged SDK.  The
# installed /usr route uses no manual include directory or producer macros.
if(NOT QA_PREFIX STREQUAL "/usr")
  target_include_directories(nsync-consumer PRIVATE "${QA_PREFIX}/include")
endif()
file(GENERATE OUTPUT "${CMAKE_BINARY_DIR}/export-usage.txt" CONTENT
  "target=${QA_LIBRARY}\ndefinitions=$<TARGET_PROPERTY:${QA_LIBRARY},INTERFACE_COMPILE_DEFINITIONS>\noptions=$<TARGET_PROPERTY:${QA_LIBRARY},INTERFACE_COMPILE_OPTIONS>\nfeatures=$<TARGET_PROPERTY:${QA_LIBRARY},INTERFACE_COMPILE_FEATURES>\nincludes=$<TARGET_PROPERTY:${QA_LIBRARY},INTERFACE_INCLUDE_DIRECTORIES>\nlink_options=$<TARGET_PROPERTY:${QA_LIBRARY},INTERFACE_LINK_OPTIONS>\nlink_libraries=$<TARGET_PROPERTY:${QA_LIBRARY},INTERFACE_LINK_LIBRARIES>\n")
if(QA_NEGATIVE)
  # Preserve actual imported usage requirements; omit only its archive.
  foreach(property IN ITEMS INTERFACE_COMPILE_DEFINITIONS INTERFACE_COMPILE_OPTIONS
      INTERFACE_COMPILE_FEATURES INTERFACE_INCLUDE_DIRECTORIES
      INTERFACE_LINK_OPTIONS INTERFACE_LINK_LIBRARIES)
    get_target_property(usage ${QA_LIBRARY} ${property})
    if(usage)
      if(property STREQUAL "INTERFACE_COMPILE_DEFINITIONS")
        target_compile_definitions(nsync-consumer PRIVATE ${usage})
      elseif(property STREQUAL "INTERFACE_COMPILE_OPTIONS")
        target_compile_options(nsync-consumer PRIVATE ${usage})
      elseif(property STREQUAL "INTERFACE_COMPILE_FEATURES")
        target_compile_features(nsync-consumer PRIVATE ${usage})
      elseif(property STREQUAL "INTERFACE_INCLUDE_DIRECTORIES")
        target_include_directories(nsync-consumer PRIVATE ${usage})
      elseif(property STREQUAL "INTERFACE_LINK_OPTIONS")
        target_link_options(nsync-consumer PRIVATE ${usage})
      elseif(property STREQUAL "INTERFACE_LINK_LIBRARIES")
        target_link_libraries(nsync-consumer PRIVATE ${usage})
      endif()
    endif()
  endforeach()
else()
  target_link_libraries(nsync-consumer PRIVATE ${QA_LIBRARY})
endif()
NSYNC_QA_CMAKELISTS_TXT
cat > .packaging-qa/expected.stdout <<'NSYNC_QA_EXPECTED_STDOUT'
PASS 1 mutex writer and reader modes
PASS 2 once executes one initializer
PASS 3 counter reaches zero without delayed wait
PASS 4 note notification propagates to child
PASS 5 time arithmetic has exact unit conversions
PASS 6 wait selects an already ready counter
NSYNC_QA_EXPECTED_STDOUT
cat > .packaging-qa/run-qa.py <<'NSYNC_QA_RUN_QA_PY'
#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Owned target-only C/C++ consumers. No library/source build or networking.
No private producer definitions are forced into either stock-export consumer.
All command/raw/map/chunk evidence survives success and failure.
"""
import argparse
import base64
import hashlib
import json
import os
import re
import shlex
import subprocess
import tempfile
from pathlib import Path

ap=argparse.ArgumentParser();ap.add_argument('--prefix',required=True);a=ap.parse_args()
Q=Path(__file__).resolve().parent;P=Path(a.prefix).resolve();W=Path(tempfile.mkdtemp(prefix='nsync-api-qa-'))
assert P.is_absolute() and (P/'lib64').is_dir()
env=dict(os.environ,LC_ALL='C',LANG='C');commands=[];chunks={};before={};after={};failure=None
cleared=['LD_LIBRARY_PATH','LD_PRELOAD','LIBRARY_PATH','CPATH','C_INCLUDE_PATH','CPLUS_INCLUDE_PATH','CMAKE_PREFIX_PATH','CMAKE_TOOLCHAIN_FILE','CMAKE_PROJECT_TOP_LEVEL_INCLUDES','CMAKE_PROJECT_INCLUDE','CMAKE_PROJECT_INCLUDE_BEFORE','CMAKE_GENERATOR','CMAKE_GENERATOR_PLATFORM','CMAKE_GENERATOR_TOOLSET','CFLAGS','CXXFLAGS','CPPFLAGS','LDFLAGS']
for key in cleared:
 env.pop(key,None)
def sha(b):return hashlib.sha256(b).hexdigest()
def remember(label,b):
 assert label not in chunks;(W/label).write_bytes(b);chunks[label]=dict(sha256=sha(b),bytes=len(b),base64=base64.b64encode(b).decode())
def run(label,argv,ok=True):
 try:result=subprocess.run(argv,cwd=W,env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
 except subprocess.TimeoutExpired as exc:
  out=exc.stdout or b'';err=exc.stderr or b'';remember(label+'.stdout',out);remember(label+'.stderr',err);commands.append(dict(label=label,argv=argv,cwd=str(W),status=None,timeout=True,stdout_sha256=sha(out),stderr_sha256=sha(err)));raise
 remember(label+'.stdout',result.stdout);remember(label+'.stderr',result.stderr);commands.append(dict(label=label,argv=argv,cwd=str(W),status=result.returncode,stdout_sha256=sha(result.stdout),stderr_sha256=sha(result.stderr),relevant_environment={k:env.get(k) for k in ['PATH','LC_ALL','LANG']},cleared_environment=cleared))
 if ok:assert result.returncode==0,(label,result.returncode)
 return result
def snapshot():
 paths=[P/'lib64/libnsync.a',P/'lib64/libnsync_cpp.a']
 header_names=['nsync.h','nsync_atomic.h','nsync_counter.h','nsync_cpp.h','nsync_cv.h','nsync_debug.h','nsync_mu.h','nsync_mu_wait.h','nsync_note.h','nsync_once.h','nsync_time.h','nsync_time_internal.h','nsync_waiter.h']
 paths += [P/'include'/v for v in header_names]
 for name in ['nsync','nsync_cpp']:
  directory=P/'lib64/cmake'/name;assert directory.is_dir() and (directory/(name+'Config.cmake')).is_file();files=sorted(directory.rglob('*'));assert files and all(not f.is_dir() or not f.is_symlink() for f in files)
  paths += [f for f in files if f.is_file()]
 paths += [Q/v for v in ['consumer.c','CMakeLists.txt','expected.stdout','run-qa.py','SHA256SUMS']]
 notices=P/'share/licenses/nsync/source-notices';assert notices.is_dir();paths += [v for v in notices.rglob('*') if v.is_file()];paths.append(P/'share/licenses/nsync/LICENSE')
 return {str(v):dict(bytes=v.stat().st_size,sha256=sha(v.read_bytes()),realpath=str(v.resolve())) for v in paths}
def samefile_trace(raw,archive):
 candidates=[]
 for line in raw.decode('utf-8',errors='strict').splitlines():
  line=line.strip()
  if line.startswith('LOAD '):line=line[5:].strip()
  if line.startswith('"') and line.endswith('"'):line=line[1:-1]
  line=line.split('(',1)[0]
  if line and Path(line).is_file() and os.path.samefile(line,archive):candidates.append(line)
 assert candidates,('No same-file archive in trace/map',str(archive));return candidates
try:
 expected=(Q/'expected.stdout').read_bytes();assert expected.count(b'PASS ')==6
 digest_rows=(Q/'SHA256SUMS').read_text().splitlines();assert len(digest_rows)==4
 for row in digest_rows:
  digest,name=row.split('  ',1);assert name in {'consumer.c','CMakeLists.txt','expected.stdout','run-qa.py'} and re.fullmatch('[a-f0-9]{64}',digest) and sha((Q/name).read_bytes())==digest
 notices=P/'share/licenses/nsync/source-notices';notice_rows=(notices/'SHA256SUMS').read_text().splitlines();assert len(notice_rows)==315
 for row in notice_rows:
  digest,name=row.split('  ',1);path=Path(name);assert re.fullmatch('[a-f0-9]{64}',digest) and not path.is_absolute() and '..' not in path.parts and name.endswith('.notice');notice=notices/path;assert notice.is_file() and not notice.is_symlink() and sha(notice.read_bytes())==digest
  if name.startswith('public/') and name.endswith('.h.notice'):assert sha((P/'include'/name[len('public/'):-len('.notice')]).read_bytes())==digest
 assert len([v for v in notices.rglob('*') if v.is_file()])==316 and sha((P/'share/licenses/nsync/LICENSE').read_bytes())=='cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30'
 before=snapshot()
 for profile,lib in [('c','libnsync.a'),('cpp','libnsync_cpp.a')]:
  archive=P/'lib64'/lib;positive=W/(profile+'-positive');negative=W/(profile+'-negative');mapfile=W/(profile+'.map')
  nm=run(profile+'-archive-symbols',['nm','-C','--defined-only',str(archive)]);assert b'nsync_mu_lock' in nm.stdout and b'nsync_counter_new' in nm.stdout and b'nsync_wait_n' in nm.stdout
  ar=run(profile+'-archive-members',['ar','t',str(archive)]);assert ar.stdout.strip()
  headers=run(profile+'-archive-ELF',['readelf','-h',str(archive)]);assert headers.stdout.count(b'Class:')>0 and headers.stdout.count(b'Class:')==headers.stdout.count(b'ELF64') and headers.stdout.count(b'Machine:')==headers.stdout.count(b'RISC-V')
  common=['cmake','-G','Unix Makefiles','-S',str(Q),'-DQA_PREFIX='+str(P),'-DQA_PROFILE='+profile,'-DQA_MAP='+str(mapfile),'-DCMAKE_BUILD_TYPE=','-DCMAKE_VERBOSE_MAKEFILE=ON','-DCMAKE_C_COMPILER=/usr/bin/gcc','-DCMAKE_CXX_COMPILER=/usr/bin/g++']
  run(profile+'-positive-configure',common+['-B',str(positive),'-DQA_NEGATIVE=OFF'])
  positive_usage=(positive/'export-usage.txt').read_bytes();remember(profile+'-positive-export-usage.txt',positive_usage)
  if profile=='cpp':assert b'NSYNC_ATOMIC_CPP11' in positive_usage and b'NSYNC_USE_CPP11_TIMEPOINT' in positive_usage
  link=run(profile+'-positive-link',['cmake','--build',str(positive),'--parallel','1']);assert link.stderr==b''
  executable=positive/'nsync-consumer';assert executable.is_file();trace=samefile_trace(link.stdout,archive);mapbytes=mapfile.read_bytes();remember(profile+'.map',mapbytes);map_paths=samefile_trace(mapbytes,archive)
  eh=run(profile+'-consumer-ELF',['readelf','-h',str(executable)]);assert b'ELF64' in eh.stdout and b'RISC-V' in eh.stdout
  dyn=run(profile+'-consumer-dynamic',['readelf','-d',str(executable)]);assert not re.search(rb'NEEDED[^\n]*libnsync',dyn.stdout)
  exe_before=sha(executable.read_bytes());output=run(profile+'-six-API-groups',[str(executable)]);assert output.stdout==expected and output.stderr==b'' and sha(executable.read_bytes())==exe_before
  remember(profile+'-consumer-binding.json',json.dumps(dict(executable=str(executable),realpath=str(executable.resolve()),sha256_before=exe_before,sha256_after=sha(executable.read_bytes()),owned_consumer_source_sha256=sha((Q/'consumer.c').read_bytes())),sort_keys=True).encode())
  # Keep the same source/profile/header configuration but omit only the
  # library target.  A generic configure/compiler failure is not evidence.
  negmap=W/(profile+'-negative.map');negcommon=[v if not v.startswith('-DQA_MAP=') else '-DQA_MAP='+str(negmap) for v in common]
  run(profile+'-negative-configure',negcommon+['-B',str(negative),'-DQA_NEGATIVE=ON'])
  negative_usage=(negative/'export-usage.txt').read_bytes();remember(profile+'-negative-export-usage.txt',negative_usage);assert positive_usage==negative_usage
  failed=run(profile+'-omitted-library-link',['cmake','--build',str(negative),'--parallel','1'],False);diagnostic=failed.stdout+failed.stderr
  assert failed.returncode!=0 and not (negative/'nsync-consumer').exists() and b'undefined reference' in diagnostic
  for anchor in [b'nsync_mu_lock',b'nsync_run_once_arg',b'nsync_counter_new',b'nsync_note_new',b'nsync_time_ms',b'nsync_wait_n']:assert anchor in diagnostic,anchor
  if negmap.exists():remember(profile+'-negative.map',negmap.read_bytes())
  remember(profile+'-same-file-proof.json',json.dumps(dict(archive=str(archive),archive_realpath=str(archive.resolve()),archive_sha256=sha(archive.read_bytes()),trace_same_file_paths=trace,map_same_file_paths=map_paths,installed_stock_export_no_producer_macro_override=True),sort_keys=True).encode())
 after=snapshot();assert before==after
except BaseException as exc:
 failure=repr(exc);raise
finally:
 report=dict(work=str(W),prefix=str(P),helper_sha256=sha(Path(__file__).read_bytes()),commands=commands,chunks=chunks,before=before,after=after,all_selected_production_and_QA_bytes_unchanged=bool(before) and before==after,failure=failure,target_only_execution=True,no_network_commands=True,no_hardware_scheduler_performance_claim=True)
 (W/'receipt.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print('NSYNC_OWNED_QA_EVIDENCE_BEGIN',flush=True);print(json.dumps(report,sort_keys=True),flush=True);print('NSYNC_OWNED_QA_EVIDENCE_END',flush=True)
NSYNC_QA_RUN_QA_PY

%build
export CFLAGS='%{optflags}'
export CXXFLAGS='%{optflags}'
export LDFLAGS='%{?build_ldflags}'
# Keep BUILD_SHARED_LIBS unset/default OFF, NSYNC_ENABLE_TESTS ON, and the
# original buildtype; do not select assembler/benchmark or shorten tests.
cmake -G 'Unix Makefiles' -S . -B .packaging-build \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_LIBDIR=%{_lib}
cmake --build .packaging-build --parallel %{?_smp_build_ncpus}%{!?_smp_build_ncpus:1}

%install
DESTDIR=%{buildroot} cmake --install .packaging-build
install -d %{buildroot}%{_datadir}/nsync-tests
for f in consumer.c CMakeLists.txt expected.stdout run-qa.py; do
  install -pm0644 .packaging-qa/"$f" %{buildroot}%{_datadir}/nsync-tests/"$f"
done
(cd %{buildroot}%{_datadir}/nsync-tests && sha256sum consumer.c CMakeLists.txt expected.stdout run-qa.py > SHA256SUMS)
install -d %{buildroot}%{_licensedir}/nsync
install -pm0644 LICENSE %{buildroot}%{_licensedir}/nsync/LICENSE
cp -a .packaging-qa/source-notices %{buildroot}%{_licensedir}/nsync/source-notices
install -Dpm0644 README %{buildroot}%{_docdir}/nsync/README

%check
export LC_ALL=C LANG=C
cmp LICENSE .packaging-qa/LICENSE.original
grep -Fx '1.30.0' VERSION
python3 - <<'PY_BEFORE'
import hashlib,json,pathlib
m=json.loads(pathlib.Path('.packaging-qa/patched-source-manifest.json').read_text())
assert len(m)==315
for p,v in m.items():
    f=pathlib.Path(p);b=f.read_bytes();assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256'] and f.stat().st_mode&0o777==v['mode']
headers=pathlib.Path('.packaging-qa/header-paths').read_text().splitlines()
assert len(headers)==13 and all(p.startswith('public/nsync') and p.endswith('.h') for p in headers)
PY_BEFORE
set +e
ctest --test-dir .packaging-build -V --output-on-failure > .packaging-qa/ctest.stdout 2> .packaging-qa/ctest.stderr
ctest_status=$?
set -e
cat .packaging-qa/ctest.stdout .packaging-qa/ctest.stderr
printf 'NSYNC_ORIGINAL_CTEST_EXIT=%%s\n' "$ctest_status"
test "$ctest_status" -eq 0
python3 - <<'PY_CTEST'
import json,pathlib,subprocess
r=subprocess.run(['ctest','--test-dir','.packaging-build','--show-only=json-v1'],check=True,stdout=subprocess.PIPE)
pathlib.Path('.packaging-qa/ctest-registered.json').write_bytes(r.stdout)
actual=json.loads(r.stdout)['tests'];assert len(actual)==26
expected=['counter_test','cv_mu_timeout_stress_test','cv_test','cv_wait_example_test','dll_test','mu_starvation_test','mu_test','mu_wait_example_test','mu_wait_test','note_test','once_test','pingpong_test','wait_test']
assert {v['name'] for v in actual}==set(expected+[v+'_cpp' for v in expected])
assert b'100%% tests passed, 0 tests failed out of 26' in pathlib.Path('.packaging-qa/ctest.stdout').read_bytes()
PY_CTEST
python3 %{buildroot}%{_datadir}/nsync-tests/run-qa.py --prefix %{buildroot}%{_prefix}
python3 - <<'PY_AFTER'
import hashlib,json,pathlib
m=json.loads(pathlib.Path('.packaging-qa/patched-source-manifest.json').read_text());assert len(m)==315
for p,v in m.items():
    f=pathlib.Path(p);b=f.read_bytes();assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256'] and f.stat().st_mode&0o777==v['mode']
print('NSYNC_314_ORIGINAL_FILES_UNCHANGED_ONE_PINNED_CMAKE_PATCH')
PY_AFTER

%files
%license %{_licensedir}/nsync
%doc %{_docdir}/nsync
%{_libdir}/libnsync.a
%{_libdir}/libnsync_cpp.a
%{_libdir}/cmake/nsync/
%{_libdir}/cmake/nsync_cpp/
%{_includedir}/nsync.h
%{_includedir}/nsync_atomic.h
%{_includedir}/nsync_counter.h
%{_includedir}/nsync_cpp.h
%{_includedir}/nsync_cv.h
%{_includedir}/nsync_debug.h
%{_includedir}/nsync_mu.h
%{_includedir}/nsync_mu_wait.h
%{_includedir}/nsync_note.h
%{_includedir}/nsync_once.h
%{_includedir}/nsync_time.h
%{_includedir}/nsync_time_internal.h
%{_includedir}/nsync_waiter.h
%{_datadir}/nsync-tests/

%changelog
* Wed Oct 28 2026 openEuler package contributors - 1.30.0-1
- Initial fixed-source SDK packaging; preserve original C/C++ static defaults
  and all 26 CTest invocations, with additive stock-export API consumers.
- Export ABI-defining C++ mode requirements PUBLIC without forcing consumer macros.
