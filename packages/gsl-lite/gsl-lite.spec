# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 openEuler package contributors.
# Upstream production SDK has no ELF; target-only consumers are built during QA.
%global debug_package %{nil}
Name:           gsl-lite
Version:        1.1.1
Release:        1%{?dist}
Summary:        Header-only defensive programming SDK for C++98 and later
License:        MIT AND BSL-1.0 AND BSD-3-Clause AND Apache-2.0
URL:            https://github.com/gsl-lite/gsl-lite
Source0:        gsl-lite-%{version}-Git.tar.gz
Source1:        Apache-2.0.txt
Source2:        BSL-1.0.txt
Source3:        BSD-3-Clause.txt

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
BuildRequires:  python3 >= 3.6
BuildRequires:  tar
Requires:       bash
Requires:       binutils
Requires:       cmake >= 3.20
Requires:       coreutils
Requires:       gcc-c++
Requires:       glibc-devel
Requires:       make
Requires:       python3 >= 3.6

%description
Guidelines-support and defensive-programming utilities. Original production
defaults remain unchanged. A separate opt-in upstream test tree preserves all
original GNU14 language/configuration variants, including genuine compile-only
targets. Installed and relocated imported-target consumers are additive QA.
No source patch, upstream pkg-config metadata, or native-RISC-V claim is made.

%prep
%setup -q -n gsl-lite-gsl-lite-b19adc1
python3 - <<'GSL_QA_SNAPSHOT'
import hashlib,json,pathlib,shutil
root=pathlib.Path('.')
assert not (root/'.packaging-qa').exists() and not (root/'.packaging-build').exists()
expected=json.loads("[{\"path\":\".editorconfig\",\"sha256\":\"ff42293a1c2782777cae9396e45957670b7b7285612774c5152d739ccf5392c3\",\"bytes\":40,\"raw_archive_mode\":\"0o664\"},{\"path\":\".gitattributes\",\"sha256\":\"9a822f9dfd37c8ac2697f84f427159011b2a9a6d582b63b508e3f1877c22c7c5\",\"bytes\":69,\"raw_archive_mode\":\"0o664\"},{\"path\":\".gitignore\",\"sha256\":\"7d57db178cea62c6285fc7fb55437646f306022ce032386eaefb698a8b269e6d\",\"bytes\":21,\"raw_archive_mode\":\"0o664\"},{\"path\":\"CHANGES.txt\",\"sha256\":\"6064a9548ec5b45958cd4f9e319d4d8c8d46e4c48d9efa790e353f52b6517240\",\"bytes\":40498,\"raw_archive_mode\":\"0o664\"},{\"path\":\"CMakeLists.txt\",\"sha256\":\"1a4b238cf2444c399a64f022d48eeca1a56e40b23941b6c1c2c57ab6614ff6ee\",\"bytes\":2124,\"raw_archive_mode\":\"0o664\"},{\"path\":\"CMakePresets.json\",\"sha256\":\"c3769e35850dd60e93802d4ef493b7a74cc5053c1a56f55eeca67a5ed91ceca4\",\"bytes\":3821,\"raw_archive_mode\":\"0o664\"},{\"path\":\"LICENSE\",\"sha256\":\"f62d346c726b63acc76c95aa1d557bf2225ea62aaf8774d97fb35c8ea7ca604b\",\"bytes\":1201,\"raw_archive_mode\":\"0o664\"},{\"path\":\"README.md\",\"sha256\":\"77e4755e7ce90ca1e62a556d65af32d77a6c76071d6f6a9e1c2bca02687eabce\",\"bytes\":23892,\"raw_archive_mode\":\"0o664\"},{\"path\":\"_config.yml\",\"sha256\":\"b94ba646460b6026dedaeae341f762ba449bad5eb5f1e19de594ff776c3a658b\",\"bytes\":181,\"raw_archive_mode\":\"0o664\"},{\"path\":\"_includes/footer.html\",\"sha256\":\"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855\",\"bytes\":0,\"raw_archive_mode\":\"0o664\"},{\"path\":\"_includes/nav-items.html\",\"sha256\":\"19e685a5f2abca68a8b233878689f0ceee0a4b690cafbed9fdc98142665b756b\",\"bytes\":231,\"raw_archive_mode\":\"0o664\"},{\"path\":\"_layouts/home.html\",\"sha256\":\"20714416d48af101459b6ba0be7326b929a000e585a2ed1aad942cf948c53498\",\"bytes\":1796,\"raw_archive_mode\":\"0o664\"},{\"path\":\"_layouts/page.html\",\"sha256\":\"a977eae01640a0ddab2e4e0026308281ceb518785ee01912da28cfea1b467793\",\"bytes\":113,\"raw_archive_mode\":\"0o664\"},{\"path\":\"_sass/minima/custom-variables.scss\",\"sha256\":\"d924b9d0798ff03d79a2fd74d394f81dfba14225647131811907b77828c9fe5b\",\"bytes\":137,\"raw_archive_mode\":\"0o664\"},{\"path\":\"appveyor.yml\",\"sha256\":\"aedbce7fe563fa7094e3d3acb3b891efbc467b6c8ef193d32cd8d9cbe1fd25bd\",\"bytes\":2013,\"raw_archive_mode\":\"0o664\"},{\"path\":\"azure-pipelines.yml\",\"sha256\":\"62f946e5f9c3901675a3a05c5009f79ec3313fa2450bc55cc73efc9f06be1d65\",\"bytes\":7354,\"raw_archive_mode\":\"0o664\"},{\"path\":\"cmake/CommonPresets.json\",\"sha256\":\"ceb4aea2295ab1d16188a11b6d22c31851e2460cf0235c980c84ac196ec2c74b\",\"bytes\":8808,\"raw_archive_mode\":\"0o664\"},{\"path\":\"cmake/InstallBasicPackageFiles.cmake\",\"sha256\":\"8b075ec5c9a90272525da820dcef248e43ddf4bb28f7e970e188ce61a9d81dc5\",\"bytes\":28252,\"raw_archive_mode\":\"0o664\"},{\"path\":\"doc/Reference.md\",\"sha256\":\"0772d78a1f3fcdc5f227984c5552d0906701ac152d6603fcdadb7af0e6d8155f\",\"bytes\":85473,\"raw_archive_mode\":\"0o664\"},{\"path\":\"example/01-basic.cpp\",\"sha256\":\"887ed7de67fc5e8479da24cb56bc23e0033352425204f8abec8df2ec343fd5cb\",\"bytes\":610,\"raw_archive_mode\":\"0o664\"},{\"path\":\"example/02-span.cpp\",\"sha256\":\"c894e599e29895b4fa2ab738916f63043576baa8b11310f66efe408cc6fe0bc0\",\"bytes\":1875,\"raw_archive_mode\":\"0o664\"},{\"path\":\"example/CMakeLists.txt\",\"sha256\":\"5404c17d1a35b78b947fd2539dd2dca06faca8dad5084e60efc0c6b5b4237ff8\",\"bytes\":668,\"raw_archive_mode\":\"0o664\"},{\"path\":\"example/with-CPM/CMakeLists.txt\",\"sha256\":\"f2cb35826d18278d29fa8204eaa976305b003cab04c1052450d4f64ecf7ff04d\",\"bytes\":660,\"raw_archive_mode\":\"0o664\"},{\"path\":\"example/with-CPM/CMakePresets.json\",\"sha256\":\"41f2ac0597fd1441e6d414c887f5f1a174c25c2955d9fb15c800b61f56257a76\",\"bytes\":369,\"raw_archive_mode\":\"0o664\"},{\"path\":\"example/with-CPM/README.md\",\"sha256\":\"fa2b6a3509bb4d34996175c696484c961172c0ff4ef270c3ac06d5867a0faa56\",\"bytes\":908,\"raw_archive_mode\":\"0o664\"},{\"path\":\"example/with-CPM/cmake/CPM.cmake\",\"sha256\":\"78ba32abdf798bc616bab7c73aac32a17bbd7b06ad9e26a6add69de8f3ae4791\",\"bytes\":42313,\"raw_archive_mode\":\"0o664\"},{\"path\":\"example/with-CPM/main.cpp\",\"sha256\":\"da0f19e068e0df77c1f432c73109153e8c73cc4a776e12e9dbcaac1932aed33f\",\"bytes\":498,\"raw_archive_mode\":\"0o664\"},{\"path\":\"example/with-Vcpkg/CMakeLists.txt\",\"sha256\":\"e976a007469a8f740a95d4ee5455f525cc28d461ab8b63b1940d598c20ecec31\",\"bytes\":464,\"raw_archive_mode\":\"0o664\"},{\"path\":\"example/with-Vcpkg/CMakePresets.json\",\"sha256\":\"b124bd4eb81692d93b7bd58328cea5750d791375fcc91cbb3bae0f3512771d9d\",\"bytes\":451,\"raw_archive_mode\":\"0o664\"},{\"path\":\"example/with-Vcpkg/README.md\",\"sha256\":\"e4703ed772cca14b440f7e5a9715b5d8b855a5f6479a20784eeefbcb00dd4692\",\"bytes\":1021,\"raw_archive_mode\":\"0o664\"},{\"path\":\"example/with-Vcpkg/main.cpp\",\"sha256\":\"da0f19e068e0df77c1f432c73109153e8c73cc4a776e12e9dbcaac1932aed33f\",\"bytes\":498,\"raw_archive_mode\":\"0o664\"},{\"path\":\"example/with-Vcpkg/vcpkg.json\",\"sha256\":\"21dc322fe52015c1494827866fe4458e6043e5aade3f27c39cf3cc5052b6e804\",\"bytes\":80,\"raw_archive_mode\":\"0o664\"},{\"path\":\"include/gsl-lite/gsl-lite.hpp\",\"sha256\":\"d5cf3a696f41c59525f125642669a1e1ea042994ca0135f8642bec5267acc410\",\"bytes\":285453,\"raw_archive_mode\":\"0o664\"},{\"path\":\"include/gsl/gsl-lite.hpp\",\"sha256\":\"c74ebe62d0083bcc8e82fde49d03239506efba6fc40586994db645971df616f5\",\"bytes\":2110,\"raw_archive_mode\":\"0o664\"},{\"path\":\"src/CMakeLists.txt\",\"sha256\":\"4a7a9467c71caabc62555ea368157ee1f6425eb18035b7d60877a4c011c1fbfe\",\"bytes\":1927,\"raw_archive_mode\":\"0o664\"},{\"path\":\"src/gsl-lite.natvis\",\"sha256\":\"19d059117c60fb1370ac613ce6f3725eb63c4b92b9c66ed8180b80ba6fb7f302\",\"bytes\":819,\"raw_archive_mode\":\"0o664\"},{\"path\":\"test/CMakeLists.txt\",\"sha256\":\"7a3a9c8f234dd0dea74bb513253b15e03af74dd2dfdaa35c04905b5e158a0686\",\"bytes\":5911,\"raw_archive_mode\":\"0o664\"},{\"path\":\"test/MakeTestTarget.cmake\",\"sha256\":\"8df2c3ef1e3bd668c2dbf1b906a91d31ee8a63c98ce1a7f9b0ec875dcc2f90e9\",\"bytes\":15304,\"raw_archive_mode\":\"0o664\"},{\"path\":\"test/assert.t.cpp\",\"sha256\":\"ca5545b73651eee1f8e213b23169ebaeee48dcfbe627c8a55d57b4bbe01960e4\",\"bytes\":11738,\"raw_archive_mode\":\"0o664\"},{\"path\":\"test/at.t.cpp\",\"sha256\":\"b3c5b28f0adbd5dea0c6bf3db4537fc460a1f0be1e8d8604290c3f37d3f79c93\",\"bytes\":4459,\"raw_archive_mode\":\"0o664\"},{\"path\":\"test/byte.t.cpp\",\"sha256\":\"e839bce06f796c9110f97e7c6a5458650c5d1670a318efd392000b371be0a1c6\",\"bytes\":6384,\"raw_archive_mode\":\"0o664\"},{\"path\":\"test/core_check.t.cpp\",\"sha256\":\"5da4540d78d0df9e1e910d3c80ba4d951dc7014fe406fe1201ccc0ba4a34e49c\",\"bytes\":2223,\"raw_archive_mode\":\"0o664\"},{\"path\":\"test/core_check_lite.t.cpp\",\"sha256\":\"6363600a6861f0106b0ddfbe304c4e9857247508917035f4620592645a5109ee\",\"bytes\":1930,\"raw_archive_mode\":\"0o664\"},{\"path\":\"test/cuda/CMakeLists.txt\",\"sha256\":\"4d23b894c5ea228d4ca93e6e379b4b0c06e9bce0560d874b3c249111ac138a80\",\"bytes\":1587,\"raw_archive_mode\":\"0o664\"},{\"path\":\"test/cuda/cuda.t.cu\",\"sha256\":\"63a265402271a2b14a3be26dbf3b34ad5bad33c12afc2927f2813552120646ec\",\"bytes\":5298,\"raw_archive_mode\":\"0o664\"},{\"path\":\"test/emulation.t.cpp\",\"sha256\":\"6cc530121c95ae1df4160784b97fcafcf3eba7b448213047e335f06a60556323\",\"bytes\":6285,\"raw_archive_mode\":\"0o664\"},{\"path\":\"test/gsl-lite.t.cpp\",\"sha256\":\"f11cbecaec0e6585ad1e98604c28a9f5e837f7ea2fb8fb32caad66566d40090d\",\"bytes\":11134,\"raw_archive_mode\":\"0o664\"},{\"path\":\"test/gsl-lite.t.hpp\",\"sha256\":\"05fedd2d46e7412f1d1d992fbea5e193fe07738d9d7cada78cdbb1905daf7a03\",\"bytes\":4936,\"raw_archive_mode\":\"0o664\"},{\"path\":\"test/issue.t.cpp\",\"sha256\":\"c81c49c289ace311f4895ec5a976403f47f21fc56ebd68b4fd90105723ec8c35\",\"bytes\":4817,\"raw_archive_mode\":\"0o664\"},{\"path\":\"test/lest_cpp03.hpp\",\"sha256\":\"ea7d0bc2871d04400d455481d0c2e1d4ebe3bfa505b6d0da2759961c9294183c\",\"bytes\":49050,\"raw_archive_mode\":\"0o664\"},{\"path\":\"test/not_null.t.cpp\",\"sha256\":\"eba02c0ee9b0a141ab74e7a39b4fd4b5008fd7748a33c2eaf3209fda6dbcdd5e\",\"bytes\":73011,\"raw_archive_mode\":\"0o664\"},{\"path\":\"test/owner.t.cpp\",\"sha256\":\"2243948d7daa1758931100bfb48576116c654d1c4f997699c6252fa9cf4abb9c\",\"bytes\":1992,\"raw_archive_mode\":\"0o664\"},{\"path\":\"test/span.t.cpp\",\"sha256\":\"000debc26923a0fb4f63c83334d90958fde08f1222ab243e00c9f120bf8310d0\",\"bytes\":66198,\"raw_archive_mode\":\"0o664\"},{\"path\":\"test/string_span.t.cpp\",\"sha256\":\"d9ed63591c8c7b75c6bf0356f06e981b69c1ad60fab9f0150ea087c253eec0e5\",\"bytes\":40419,\"raw_archive_mode\":\"0o664\"},{\"path\":\"test/util.t.cpp\",\"sha256\":\"97b99c770635126c74b72ad9b9c3711adcc753e00c99015ff35148bf8653ecfd\",\"bytes\":33709,\"raw_archive_mode\":\"0o664\"}]")
actual=sorted(p.as_posix() for p in root.rglob('*') if p.is_file())
assert len(actual)==55 and set(actual)=={r['path'] for r in expected}
q=root/'.packaging-qa';q.mkdir()
manifest={}
for row in expected:
    p=root/row['path'];raw=p.read_bytes();assert not p.is_symlink()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
    mode=p.stat().st_mode&0o777;assert not mode&0o111
    manifest[row['path']]=dict(sha256=row['sha256'],bytes=row['bytes'],raw_archive_mode=row['raw_archive_mode'],extracted_mode=mode)
    dest=q/'source-notices'/(row['path']+'.notice');dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
(q/'original-source-manifest.json').write_text(json.dumps(manifest,sort_keys=True)+'\n')
(q/'source-notices/SHA256SUMS').write_text(''.join(r['sha256']+'  '+p+'.notice\n' for p,r in sorted(manifest.items())))
for source,name,want in [
    ('%{SOURCE1}','Apache-2.0.txt','cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30'),
    ('%{SOURCE2}','BSL-1.0.txt','84c6ef3ea9e3254a54d0acf5d3e0c61ae011b8fef7dd6940591cf060e6380a8f'),
    ('%{SOURCE3}','BSD-3-Clause.txt','5a93d5831e1297ab10fe643e1a631e83be392896da14ee2951285a79012df69d')]:
    raw=pathlib.Path(source).read_bytes();assert hashlib.sha256(raw).hexdigest()==want
    (q/name).write_bytes(raw)
GSL_QA_SNAPSHOT
cat > .packaging-qa/consumer.cpp <<'GSL_OWNED_0'
/* Copyright 2026 openEuler package contributors.
 * SPDX-License-Identifier: Apache-2.0
 * Full grant is shipped separately as Apache-2.0.txt; upstream grants unchanged.
 */
#include <iostream>
#include <cstring>
#if QA_LEGACY_HEADER
# include <gsl/gsl-lite.hpp>
#else
# include <gsl-lite/gsl-lite.hpp>
#endif
extern int gsl_peer();
typedef char defaults_must_match[(gsl_CONFIG_DEFAULTS_VERSION == QA_DEFAULTS) ? 1 : -1];
int main()
{
    if (gsl_lite_MAJOR != 1 || gsl_lite_MINOR != 1 || gsl_lite_PATCH != 1) return 10;
    int data[4] = { 2, 4, 6, 8 };
    gsl_lite::span<int> view(data, 4);
    if (view.size() != 4 || view[1] != 4 || view.subspan(1, 2).size() != 2) return 11;
    gsl_lite::not_null<int*> pointer(&data[0]);
    *pointer = 3;
    if (data[0] != 3 || gsl_lite::at(data, 2) != 6) return 12;
    if (gsl_lite::narrow<int>(123L) != 123 || gsl_lite::narrow_cast<int>(4L) != 4) return 13;
    if (gsl_lite::narrow_failfast<unsigned char>(42) != 42 || gsl_peer() != 32) return 14;
    int negative = 0;
    try { gsl_Expects(false); } catch (gsl_lite::fail_fast const&) { ++negative; }
    try { (void)gsl_lite::at(data, 99); } catch (gsl_lite::fail_fast const&) { ++negative; }
    try { (void)gsl_lite::narrow_failfast<unsigned char>(1000); } catch (gsl_lite::fail_fast const&) { ++negative; }
    if (negative != 3) return 15;
    std::cout << "gsl-lite-owned-ok defaults=" << gsl_CONFIG_DEFAULTS_VERSION
              << " header=" << QA_LEGACY_HEADER << " std=" << QA_STD
              << " route=" << QA_ROUTE << " positive-groups=5 negative-contracts=3 multi-tu=1\n";
    return 0;
}
GSL_OWNED_0
cat > .packaging-qa/peer.cpp <<'GSL_OWNED_1'
/* Copyright 2026 openEuler package contributors.
 * SPDX-License-Identifier: Apache-2.0
 */
#if QA_LEGACY_HEADER
# include <gsl/gsl-lite.hpp>
#else
# include <gsl-lite/gsl-lite.hpp>
#endif
typedef char peer_defaults_must_match[(gsl_CONFIG_DEFAULTS_VERSION == QA_DEFAULTS) ? 1 : -1];
int gsl_peer()
{
    int data[2] = {10, 20};
    gsl_lite::span<int> view(data, 2);
    return gsl_lite::narrow<int>(view.size()) + gsl_lite::at(data, 0) + gsl_lite::at(data, 1);
}
GSL_OWNED_1
cat > .packaging-qa/CMakeLists.txt <<'GSL_OWNED_2'
# Copyright 2026 openEuler package contributors.
# SPDX-License-Identifier: Apache-2.0
cmake_minimum_required(VERSION 3.20)
project(gsl_lite_installed_qa LANGUAGES CXX)
if(NOT DEFINED QA_PREFIX OR NOT IS_ABSOLUTE "${QA_PREFIX}")
  message(FATAL_ERROR "QA_PREFIX must name the exact installed or relocated SDK")
endif()
set(CMAKE_FIND_USE_PACKAGE_REGISTRY OFF)
set(CMAKE_FIND_USE_SYSTEM_PACKAGE_REGISTRY OFF)
find_package(gsl-lite 1.1.1 EXACT CONFIG REQUIRED
  PATHS "${QA_PREFIX}/share/cmake/gsl-lite" NO_DEFAULT_PATH)
set(routes gsl-lite::gsl-lite gsl-lite::gsl-lite-v0 gsl-lite::gsl-lite-v1
           gsl::gsl-lite gsl::gsl-lite-v0 gsl::gsl-lite-v1)
set(route_number 0)
foreach(route IN LISTS routes)
  if(NOT TARGET "${route}")
    message(FATAL_ERROR "Missing imported target/alias ${route}")
  endif()
  get_target_property(includes "${route}" INTERFACE_INCLUDE_DIRECTORIES)
  foreach(include IN LISTS includes)
    if(NOT include STREQUAL "${QA_PREFIX}/include")
      message(FATAL_ERROR "Unexpected installed include path for ${route}: ${include}")
    endif()
  endforeach()
  if(NOT includes)
    message(FATAL_ERROR "Missing installed include path for ${route}")
  endif()
  set(defaults 1)
  if(route MATCHES "-v0$")
    set(defaults 0)
  endif()
  foreach(header IN ITEMS 0 1)
    foreach(standard IN ITEMS 98 17 23)
      set(name "gsl-qa-r${route_number}-h${header}-s${standard}")
      add_executable("${name}" consumer.cpp peer.cpp)
      set_target_properties("${name}" PROPERTIES CXX_STANDARD "${standard}"
        CXX_STANDARD_REQUIRED YES CXX_EXTENSIONS NO)
      target_compile_definitions("${name}" PRIVATE
        "QA_DEFAULTS=${defaults}" "QA_LEGACY_HEADER=${header}" "QA_STD=${standard}"
        "QA_ROUTE=${route_number}" gsl_CONFIG_CONTRACT_VIOLATION_THROWS
        gsl_CONFIG_CONTRACT_CHECKING_AUDIT gsl_CONFIG_ACKNOWLEDGE_NONSTANDARD_ABI)
      if(header)
        target_compile_definitions("${name}" PRIVATE gsl_FEATURE_GSL_COMPATIBILITY_MODE=1)
      endif()
      target_compile_options("${name}" PRIVATE -H)
      target_link_libraries("${name}" PRIVATE "${route}")
    endforeach()
  endforeach()
  math(EXPR route_number "${route_number}+1")
endforeach()
GSL_OWNED_2
cat > .packaging-qa/run-installed.py <<'GSL_OWNED_3'
#!/usr/bin/env python3
# Copyright 2026 openEuler package contributors.
# SPDX-License-Identifier: Apache-2.0
import argparse,base64,hashlib,json,os,pathlib,re,shutil,subprocess
ap=argparse.ArgumentParser();ap.add_argument('--prefix',required=True);ap.add_argument('--work-dir',required=True);a=ap.parse_args()
P=pathlib.Path(a.prefix).resolve();W=pathlib.Path(a.work_dir).absolute();Q=pathlib.Path(__file__).resolve().parent
assert P.is_dir() and P.is_absolute() and not W.exists();W.mkdir(parents=True,mode=0o700)
invocation='gsl-qa-'+hashlib.sha256(str(W).encode('utf-8')).hexdigest()[:16]
headers={'gsl-lite/gsl-lite.hpp':'d5cf3a696f41c59525f125642669a1e1ea042994ca0135f8642bec5267acc410','gsl/gsl-lite.hpp':'c74ebe62d0083bcc8e82fde49d03239506efba6fc40586994db645971df616f5'}
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for path,row in json.loads((Q/'owned-files.json').read_bytes()).items():
 p=Q/path;assert p.is_file() and not p.is_symlink() and digest(p)==row['sha256'] and p.stat().st_size==row['bytes'],path
assert digest(Q/'Apache-2.0.txt')=='cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30'
original=json.loads((Q/'original-source-manifest.json').read_bytes());assert len(original)==55
for path,row in original.items():
 p=Q/'source-notices'/(path+'.notice');assert p.is_file() and not p.is_symlink() and digest(p)==row['sha256'] and p.stat().st_size==row['bytes']
env=dict(os.environ);env.update(CMAKE_PREFIX_PATH='',CMAKE_MODULE_PATH='',PKG_CONFIG_PATH='',LC_ALL='C')
commands=[]
def emit_raw(label,stream,raw):
 size=1536;count=max(1,(len(raw)+size-1)//size)
 common=dict(invocation=invocation,label=label,stream=stream,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),chunks=count,encoding='base64',chunk_max_decoded_bytes=size)
 print('GSL_QA_RAW_BEGIN '+json.dumps(common,sort_keys=True),flush=True)
 for index in range(count):
  part=raw[index*size:(index+1)*size]
  print('GSL_QA_RAW_CHUNK '+json.dumps(dict(common,index=index,decoded_bytes=len(part),payload=base64.b64encode(part).decode('ascii')),sort_keys=True),flush=True)
 print('GSL_QA_RAW_END '+json.dumps(common,sort_keys=True),flush=True)
def capture(label,args,code,stdout,stderr,expected,timed_out=False):
 (W/(label+'.stdout')).write_bytes(stdout);(W/(label+'.stderr')).write_bytes(stderr)
 row=dict(label=label,args=args,exit=code,expected_exit='nonzero' if expected is None else expected,timed_out=timed_out,stdout_sha256=hashlib.sha256(stdout).hexdigest(),stdout_bytes=len(stdout),stderr_sha256=hashlib.sha256(stderr).hexdigest(),stderr_bytes=len(stderr),raw_outer_log_encoding='GSL_QA_RAW_BEGIN/CHUNK/END base64',all_raw_chunks_emitted=True)
 commands.append(row)
 emit_raw(label,'stdout',stdout);emit_raw(label,'stderr',stderr)
def run(label,args,expected=0,timeout=1800):
 try:p=subprocess.run(args,env=env,cwd=W,capture_output=True,timeout=timeout)
 except subprocess.TimeoutExpired as failure:
  capture(label,args,None,failure.stdout or b'',failure.stderr or b'',expected,timed_out=True);raise
 capture(label,args,p.returncode,p.stdout,p.stderr,expected)
 assert (p.returncode!=0 if expected is None else p.returncode==expected),(label,p.returncode,p.stdout[-3000:],p.stderr[-3000:])
 return subprocess.CompletedProcess(p.args,p.returncode,p.stdout.decode('utf-8'),p.stderr.decode('utf-8'))
def validate_headers(prefix):
 for rel,want in headers.items():
  p=prefix/'include'/rel;assert p.is_file() and not p.is_symlink() and digest(p)==want
 for name in ['gsl-liteConfig.cmake','gsl-liteConfigVersion.cmake','gsl-liteTargets.cmake']:
  p=prefix/'share/cmake/gsl-lite'/name;assert p.is_file() and not p.is_symlink()
validate_headers(P);results=[]
for label,prefix in [('installed',P),('relocated',W/'relocated-prefix')]:
 if label=='relocated':
  for rel in headers:
   src=P/'include'/rel;dest=prefix/'include'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
  dest=prefix/'share/cmake/gsl-lite';dest.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(P/'share/cmake/gsl-lite',dest,symlinks=False)
  validate_headers(prefix)
 src=W/(label+'-src');src.mkdir();build=W/(label+'-build')
 for name in ['CMakeLists.txt','consumer.cpp','peer.cpp']:shutil.copyfile(Q/name,src/name)
 run(label+'-configure',['cmake','-S',str(src),'-B',str(build),'-G','Unix Makefiles','-DQA_PREFIX='+str(prefix),'-DCMAKE_EXPORT_COMPILE_COMMANDS=ON','-DCMAKE_EXPORT_PACKAGE_REGISTRY=OFF','-DCMAKE_FIND_USE_PACKAGE_REGISTRY=OFF','-DCMAKE_FIND_USE_SYSTEM_PACKAGE_REGISTRY=OFF'])
 output=run(label+'-build',['cmake','--build',str(build),'--parallel','2','--verbose'])
 seen={};trace=output.stdout+'\n'+output.stderr
 for rel,want in headers.items():
  hits=[]
  for line in trace.splitlines():
   m=re.match(r'^\.+\s+(/.*)$',line)
   if m and m.group(1).endswith('/'+rel):
    p=pathlib.Path(m.group(1));assert p.resolve()==(prefix/'include'/rel).resolve() and digest(p)==want;hits.append(str(p))
  assert hits,(label,rel,'No same-file compiler include trace');seen[rel]=sorted(set(hits))
 entries=json.loads((build/'compile_commands.json').read_bytes());assert len(entries)==72 and {pathlib.Path(r['file']).name for r in entries}=={'consumer.cpp','peer.cpp'}
 executables=[]
 for route in range(6):
  for header in [0,1]:
   for standard in [98,17,23]:
    name='gsl-qa-r%%d-h%%d-s%%d'%%(route,header,standard);exe=build/name;assert exe.is_file() and not exe.is_symlink();elf=run(label+'-'+name+'-elf',['readelf','-h',str(exe)]).stdout;assert 'ELF64' in elf and "2's complement, little endian" in elf and re.search(r'Machine:\s+RISC-V',elf)
    expected='gsl-lite-owned-ok defaults=%%d header=%%d std=%%d route=%%d positive-groups=5 negative-contracts=3 multi-tu=1'%%(0 if route in [1,4] else 1,header,standard,route);result=run(label+'-'+name,[str(exe)]);assert result.stdout.strip()==expected and not result.stderr;executables.append(dict(name=name,sha256=digest(exe),bytes=exe.stat().st_size,stdout=expected,ELF64_little_endian_RISC_V=True))
 # The installed config must not silently fall back to a system/source package.
 bad=W/(label+'-missing-prefix');missing=run(label+'-missing-prefix',['cmake','-S',str(src),'-B',str(W/(label+'-negative-build')),'-DQA_PREFIX='+str(bad)],expected=None,timeout=120)
 diagnostic=missing.stdout+missing.stderr
 assert 'Could not find a package configuration file provided by' in diagnostic and 'gsl-liteConfig.cmake' in diagnostic and 'gsl-lite' in diagnostic
 results.append(dict(prefix=str(prefix),executables=executables,header_traces=seen,missing_prefix_rejected=True))
result=dict(status='passed',invocation_id=invocation,routes=6,headers=2,standards=[98,17,23],prefix_modes=2,executed_consumers=72,compiled_translation_units=144,all_original_notice_snapshots=55,owned_QA_does_not_replace_original_upstream_matrix=True,results=results,commands=commands)
result['full_command_raw_streams_captured_in_outer_log']=True
result['source_header_and_ELF_metadata_tied_to_exact_run_stream_hashes']=True
encoded=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode('utf-8')
(W/'result.json').write_bytes(encoded);emit_raw('complete-installed-sdk-QA','result-json',encoded)
print(json.dumps(dict(status='passed',executed_consumers=72,original_notices=55,result=str(W/'result.json'),result_sha256=hashlib.sha256(encoded).hexdigest(),full_result_and_raw_streams_in_outer_log=True)))
GSL_OWNED_3
cat > .packaging-qa/upstream-audit.py <<'GSL_OWNED_4'
#!/usr/bin/env python3
# Copyright 2026 openEuler package contributors.
# SPDX-License-Identifier: Apache-2.0
import hashlib,json,pathlib,re,shlex,subprocess,sys
R=pathlib.Path('.').resolve();Q=R/'.packaging-qa';B=R/'.packaging-build/tests';registry=json.loads((Q/'test-registry.json').read_bytes());original=json.loads((Q/'original-source-manifest.json').read_bytes())
def check_original():
 assert len(original)==55
 for path,row in original.items():
  p=R/path;raw=p.read_bytes();assert not p.is_symlink() and len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'] and p.stat().st_mode&0o777==row['extracted_mode']
check_original();commands=[]
def run(label,args):
 p=subprocess.run(args,cwd=R,capture_output=True,text=True,timeout=7200);(Q/(label+'.stdout')).write_text(p.stdout);(Q/(label+'.stderr')).write_text(p.stderr);sys.stdout.write(p.stdout);sys.stderr.write(p.stderr);commands.append(dict(label=label,args=args,exit=p.returncode,stdout_sha256=hashlib.sha256(p.stdout.encode()).hexdigest(),stderr_sha256=hashlib.sha256(p.stderr.encode()).hexdigest()));assert p.returncode==0,(label,p.returncode);return p
entries=json.loads((B/'compile_commands.json').read_bytes());seen={row['name']:set() for row in registry};compilers=set()
for entry in entries:
 args=entry.get('arguments') or shlex.split(entry['command']);source=pathlib.Path(entry['file']).resolve();name=next((row['name'] for row in registry if any('CMakeFiles/'+row['name']+'.dir/' in arg for arg in args)),None)
 if name is None:raise AssertionError('Unexpected non-original compile target')
 compilers.add(args[0]);row=next(row for row in registry if row['name']==name);assert '-std=c++'+str(row['standard']) in args and '-Werror' in args and '-fno-elide-constructors' in args and '-fstrict-aliasing' in args
 if row['family']=='gsl-lite-v1-no-exc':assert '-fno-exceptions' in args
 if source.name=='cmake_pch.hxx.cxx':continue
 relative=source.relative_to(R).as_posix();assert relative in row['sources'] and relative not in seen[name];seen[name].add(relative)
assert len(compilers)==1;compiler=next(iter(compilers));version=run('upstream-compiler-version',[compiler,'-dumpfullversion','-dumpversion']).stdout.strip();numbers=tuple(int(v) for v in version.split('.'));assert (14,)<=numbers<(15,),('Compiler migration needs an explicit new original-matrix audit',version)
archive_text=run('stacktrace-exp-archive-path',[compiler,'-print-file-name=libstdc++exp.a']).stdout.strip()
archive=pathlib.Path(archive_text);expected_archive=pathlib.Path('/usr/lib/gcc/riscv64-openEuler-linux/14/libstdc++exp.a')
assert archive.is_absolute() and archive.is_file() and archive.resolve()==expected_archive.resolve()
archive_bytes=archive.read_bytes();assert archive_bytes.startswith(b'!<arch>\n') and len(archive_bytes)>8
archive_elf=run('stacktrace-exp-archive-ELF',['readelf','-h',str(archive)]).stdout
machines=re.findall(r'Machine:\s+([^\n]+)',archive_elf);classes=re.findall(r'Class:\s+(\S+)',archive_elf);orders=re.findall(r'Data:\s+([^\n]+)',archive_elf);types=re.findall(r'Type:\s+(\S+)',archive_elf)
assert machines and len(machines)==len(classes)==len(orders)==len(types) and all(v.strip()=='RISC-V' for v in machines) and all(v=='ELF64' for v in classes) and all("2's complement, little endian" in v for v in orders) and all(v=='REL' for v in types)
linkfile=B/'test/CMakeFiles/gsl-lite-v1-stacktrace-cpp23.t.dir/link.txt';linktext=linkfile.read_text();assert '-lstdc++exp' in shlex.split(linktext)
print('GSL_LITE_ORIGINAL_STACKTRACE_LINK_COMMAND '+linktext)
stacktrace_input=dict(compiler_path=compiler,compiler_version=version,archive_path=str(archive),archive_sha256=hashlib.sha256(archive_bytes).hexdigest(),archive_bytes=len(archive_bytes),RISC_V_ELF64LE_relocatable_members=len(machines),original_link_command=linktext,compile_only_not_unwinding_runtime_coverage=True)
assert len(registry)==52 and sum(not row['compile_only'] for row in registry)==15 and sum(row['compile_only'] for row in registry)==37
for row in registry:
 assert seen[row['name']]==set(row['sources']);binary=B/'test'/row['name'];assert binary.is_file() and not binary.is_symlink();elf=run('upstream-'+row['name']+'-ELF',['readelf','-h',str(binary)]).stdout;assert 'ELF64' in elf and "2's complement, little endian" in elf and re.search(r'Machine:\s+RISC-V',elf)
listing=json.loads(run('upstream-ctest-list',['ctest','--test-dir',str(B),'--show-only=json-v1']).stdout);runtime=sorted(row['name'] for row in registry if not row['compile_only']);assert sorted(v['name'] for v in listing['tests'])==runtime and len(listing['tests'])==15
for row in listing['tests']:assert row['command']==[str(B/'test'/row['name'])] and not any(p['name'] in ['DISABLED','SKIP_RETURN_CODE'] for p in row.get('properties',[]))
output=run('upstream-ctest',['ctest','--test-dir',str(B),'-V','--output-on-failure']);assert '100%% tests passed, 0 tests failed out of 15' in output.stdout and len(re.findall(r'Test\s+#\d+:.*?\sPassed\s',output.stdout))==15 and not re.search(r'\*\*\*(?:Not Run|Skipped|Failed)',output.stdout+output.stderr)
check_original();result=dict(status='passed',compiler=compiler,compiler_version=version,original_files_unchanged=55,compiled_original_targets=52,upstream_compile_only_not_executed=37,unfiltered_original_CTest_entries_passed=15,source_CASE_counts_not_runtime_counts=True,original_GNU14_stacktrace_branch_compiled_and_linked=True,stacktrace_link_input=stacktrace_input,commands=commands);(Q/'upstream-result.json').write_text(json.dumps(result,indent=2)+'\n');print('GSL_LITE_ORIGINAL_52_TARGETS_15_CTESTS_37_COMPILE_ONLY_55_FILES_UNCHANGED')
GSL_OWNED_4
cat > .packaging-qa/test-registry.json <<'GSL_ORIGINAL_TEST_REGISTRY'
[{"name":"gsl-lite-v0-cpp98.t","standard":98,"family":"gsl-lite-v0","compile_only":false,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp","test/at.t.cpp","test/byte.t.cpp","test/emulation.t.cpp","test/issue.t.cpp","test/not_null.t.cpp","test/owner.t.cpp","test/span.t.cpp","test/string_span.t.cpp","test/util.t.cpp"],"defaults":"v0"},{"name":"gsl-lite-v0-cpp11.t","standard":11,"family":"gsl-lite-v0","compile_only":false,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp","test/at.t.cpp","test/byte.t.cpp","test/emulation.t.cpp","test/issue.t.cpp","test/not_null.t.cpp","test/owner.t.cpp","test/span.t.cpp","test/string_span.t.cpp","test/util.t.cpp"],"defaults":"v0"},{"name":"gsl-lite-v0-cpp14.t","standard":14,"family":"gsl-lite-v0","compile_only":false,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp","test/at.t.cpp","test/byte.t.cpp","test/emulation.t.cpp","test/issue.t.cpp","test/not_null.t.cpp","test/owner.t.cpp","test/span.t.cpp","test/string_span.t.cpp","test/util.t.cpp"],"defaults":"v0"},{"name":"gsl-lite-v0-cpp17.t","standard":17,"family":"gsl-lite-v0","compile_only":false,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp","test/at.t.cpp","test/byte.t.cpp","test/emulation.t.cpp","test/issue.t.cpp","test/not_null.t.cpp","test/owner.t.cpp","test/span.t.cpp","test/string_span.t.cpp","test/util.t.cpp"],"defaults":"v0"},{"name":"gsl-lite-v0-cpp20.t","standard":20,"family":"gsl-lite-v0","compile_only":false,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp","test/at.t.cpp","test/byte.t.cpp","test/emulation.t.cpp","test/issue.t.cpp","test/not_null.t.cpp","test/owner.t.cpp","test/span.t.cpp","test/string_span.t.cpp","test/util.t.cpp"],"defaults":"v0"},{"name":"gsl-lite-v0-cpp23.t","standard":23,"family":"gsl-lite-v0","compile_only":false,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp","test/at.t.cpp","test/byte.t.cpp","test/emulation.t.cpp","test/issue.t.cpp","test/not_null.t.cpp","test/owner.t.cpp","test/span.t.cpp","test/string_span.t.cpp","test/util.t.cpp"],"defaults":"v0"},{"name":"gsl-lite-v1-cpp98.t","standard":98,"family":"gsl-lite-v1","compile_only":false,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp","test/at.t.cpp","test/byte.t.cpp","test/emulation.t.cpp","test/issue.t.cpp","test/not_null.t.cpp","test/owner.t.cpp","test/span.t.cpp","test/string_span.t.cpp","test/util.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-cpp11.t","standard":11,"family":"gsl-lite-v1","compile_only":false,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp","test/at.t.cpp","test/byte.t.cpp","test/emulation.t.cpp","test/issue.t.cpp","test/not_null.t.cpp","test/owner.t.cpp","test/span.t.cpp","test/string_span.t.cpp","test/util.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-cpp14.t","standard":14,"family":"gsl-lite-v1","compile_only":false,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp","test/at.t.cpp","test/byte.t.cpp","test/emulation.t.cpp","test/issue.t.cpp","test/not_null.t.cpp","test/owner.t.cpp","test/span.t.cpp","test/string_span.t.cpp","test/util.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-cpp17.t","standard":17,"family":"gsl-lite-v1","compile_only":false,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp","test/at.t.cpp","test/byte.t.cpp","test/emulation.t.cpp","test/issue.t.cpp","test/not_null.t.cpp","test/owner.t.cpp","test/span.t.cpp","test/string_span.t.cpp","test/util.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-cpp20.t","standard":20,"family":"gsl-lite-v1","compile_only":false,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp","test/at.t.cpp","test/byte.t.cpp","test/emulation.t.cpp","test/issue.t.cpp","test/not_null.t.cpp","test/owner.t.cpp","test/span.t.cpp","test/string_span.t.cpp","test/util.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-cpp23.t","standard":23,"family":"gsl-lite-v1","compile_only":false,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp","test/at.t.cpp","test/byte.t.cpp","test/emulation.t.cpp","test/issue.t.cpp","test/not_null.t.cpp","test/owner.t.cpp","test/span.t.cpp","test/string_span.t.cpp","test/util.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-no-exc-cpp98.t","standard":98,"family":"gsl-lite-v1-no-exc","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp","test/at.t.cpp","test/byte.t.cpp","test/emulation.t.cpp","test/issue.t.cpp","test/not_null.t.cpp","test/owner.t.cpp","test/span.t.cpp","test/string_span.t.cpp","test/util.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-no-exc-cpp11.t","standard":11,"family":"gsl-lite-v1-no-exc","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp","test/at.t.cpp","test/byte.t.cpp","test/emulation.t.cpp","test/issue.t.cpp","test/not_null.t.cpp","test/owner.t.cpp","test/span.t.cpp","test/string_span.t.cpp","test/util.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-no-exc-cpp14.t","standard":14,"family":"gsl-lite-v1-no-exc","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp","test/at.t.cpp","test/byte.t.cpp","test/emulation.t.cpp","test/issue.t.cpp","test/not_null.t.cpp","test/owner.t.cpp","test/span.t.cpp","test/string_span.t.cpp","test/util.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-no-exc-cpp17.t","standard":17,"family":"gsl-lite-v1-no-exc","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp","test/at.t.cpp","test/byte.t.cpp","test/emulation.t.cpp","test/issue.t.cpp","test/not_null.t.cpp","test/owner.t.cpp","test/span.t.cpp","test/string_span.t.cpp","test/util.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-no-exc-cpp20.t","standard":20,"family":"gsl-lite-v1-no-exc","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp","test/at.t.cpp","test/byte.t.cpp","test/emulation.t.cpp","test/issue.t.cpp","test/not_null.t.cpp","test/owner.t.cpp","test/span.t.cpp","test/string_span.t.cpp","test/util.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-no-exc-cpp23.t","standard":23,"family":"gsl-lite-v1-no-exc","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp","test/at.t.cpp","test/byte.t.cpp","test/emulation.t.cpp","test/issue.t.cpp","test/not_null.t.cpp","test/owner.t.cpp","test/span.t.cpp","test/string_span.t.cpp","test/util.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-special-cpp98.t","standard":98,"family":"gsl-lite-v1-special","compile_only":false,"sources":["test/gsl-lite.t.cpp","test/not_null.t.cpp","test/util.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-special-cpp11.t","standard":11,"family":"gsl-lite-v1-special","compile_only":false,"sources":["test/gsl-lite.t.cpp","test/not_null.t.cpp","test/util.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-special-cpp14.t","standard":14,"family":"gsl-lite-v1-special","compile_only":false,"sources":["test/gsl-lite.t.cpp","test/not_null.t.cpp","test/util.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-unenforced-cpp98.t","standard":98,"family":"gsl-lite-v1-unenforced","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-unenforced-cpp11.t","standard":11,"family":"gsl-lite-v1-unenforced","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-unenforced-cpp14.t","standard":14,"family":"gsl-lite-v1-unenforced","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-unenforced-cpp17.t","standard":17,"family":"gsl-lite-v1-unenforced","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-unenforced-cpp20.t","standard":20,"family":"gsl-lite-v1-unenforced","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-assume-cpp98.t","standard":98,"family":"gsl-lite-v1-assume","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-assume-cpp11.t","standard":11,"family":"gsl-lite-v1-assume","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-assume-cpp14.t","standard":14,"family":"gsl-lite-v1-assume","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-assume-cpp17.t","standard":17,"family":"gsl-lite-v1-assume","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-assume-cpp20.t","standard":20,"family":"gsl-lite-v1-assume","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-stacktrace-cpp23.t","standard":23,"family":"gsl-lite-v1-stacktrace","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-terminates-cpp98.t","standard":98,"family":"gsl-lite-v1-terminates","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-terminates-cpp11.t","standard":11,"family":"gsl-lite-v1-terminates","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-terminates-cpp14.t","standard":14,"family":"gsl-lite-v1-terminates","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-terminates-cpp17.t","standard":17,"family":"gsl-lite-v1-terminates","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-terminates-cpp20.t","standard":20,"family":"gsl-lite-v1-terminates","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-asserts-cpp98.t","standard":98,"family":"gsl-lite-v1-asserts","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-asserts-cpp11.t","standard":11,"family":"gsl-lite-v1-asserts","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-asserts-cpp14.t","standard":14,"family":"gsl-lite-v1-asserts","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-asserts-cpp17.t","standard":17,"family":"gsl-lite-v1-asserts","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-asserts-cpp20.t","standard":20,"family":"gsl-lite-v1-asserts","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-calls-handler-cpp98.t","standard":98,"family":"gsl-lite-v1-calls-handler","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-calls-handler-cpp11.t","standard":11,"family":"gsl-lite-v1-calls-handler","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-calls-handler-cpp14.t","standard":14,"family":"gsl-lite-v1-calls-handler","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-calls-handler-cpp17.t","standard":17,"family":"gsl-lite-v1-calls-handler","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-calls-handler-cpp20.t","standard":20,"family":"gsl-lite-v1-calls-handler","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-traps-cpp98.t","standard":98,"family":"gsl-lite-v1-traps","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-traps-cpp11.t","standard":11,"family":"gsl-lite-v1-traps","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-traps-cpp14.t","standard":14,"family":"gsl-lite-v1-traps","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-traps-cpp17.t","standard":17,"family":"gsl-lite-v1-traps","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"},{"name":"gsl-lite-v1-traps-cpp20.t","standard":20,"family":"gsl-lite-v1-traps","compile_only":true,"sources":["test/gsl-lite.t.cpp","test/assert.t.cpp"],"defaults":"v1"}]
GSL_ORIGINAL_TEST_REGISTRY
python3 - <<'GSL_FULL_LICENSE_BUNDLE_B64'
import base64,hashlib,pathlib
encoded=(
    'R1NMLWxpdGUxLjEuMSBvcmlnaW5hbCBub3RpY2VzIGFuZCBsaWNlbnNlIHRlcm1zCkZpeGVkIHNv'
    'dXJjZSBiMTlhZGMxZmZlNjFiMDVkOGM4ODU4ZGM4MjRlZGI3YzE1ZGE2OGZjOyBzb3VyY2UgYXJj'
    'aGl2ZSBTSEEyNTYgNzJiNDhhZGEwMTkwMjI5ZGJkNjVjZGQ2MzdmMDkyMzQwZTM5NzAwNGQ2OWJh'
    'NzUxZjA0Y2Q4ZDE5NTc0YTMxNgoKVGhlIHN0YW5kYXJkIFNQRFggY29weXJpZ2h0IHBsYWNlaG9s'
    'ZGVycyBiZWxvdyBhcmUgcmV0YWluZWQgYXMgZXhhbXBsZXMsIG5vdCBhc3NlcnRlZCBhcyBwcm9q'
    'ZWN0IGNvcHlyaWdodCBob2xkZXJzLiBUaGUgYWN0dWFsIG9yaWdpbmFsIHBlci1maWxlIG5vdGlj'
    'ZXMgYXJlIGF1dGhvcml0YXRpdmUgYW5kIGFsbDU1IG9yaWdpbmFsIGZpbGVzIG11c3QgYWxzbyBy'
    'ZW1haW4gYXZhaWxhYmxlIGFzIG5vdGljZSBzbmFwc2hvdHMuIE93bmVkIFFBIGhhcyBhIHNlcGFy'
    'YXRlIEFwYWNoZS0yLjAgZ3JhbnQgYW5kIGRvZXMgbm90IHJlbGljZW5zZSBhbnkgc291cmNlLgoK'
    'PT09PT0gUm9vdCBwcm9qZWN0IE1JVCBncmFudCAob3JpZ2luYWwgTElDRU5TRSwgYnl0ZS1pZGVu'
    'dGljYWwgdGV4dCkgPT09PT0K77u/VGhlIE1JVCBMaWNlbnNlIChNSVQpCgpDb3B5cmlnaHQgKGMp'
    'IDIwMTUtMjAxOSBNYXJ0aW4gTW9lbmUKQ29weXJpZ2h0IChjKSAyMDE5LTIwMjUgTW9yaXR6IEJl'
    'dXRlbApDb3B5cmlnaHQgKGMpIDIwMTUtMjAxOCwgMjAyNSBNaWNyb3NvZnQgQ29ycG9yYXRpb24u'
    'IEFsbCByaWdodHMgcmVzZXJ2ZWQuIAoKUGVybWlzc2lvbiBpcyBoZXJlYnkgZ3JhbnRlZCwgZnJl'
    'ZSBvZiBjaGFyZ2UsIHRvIGFueSBwZXJzb24gb2J0YWluaW5nIGEgY29weQpvZiB0aGlzIHNvZnR3'
    'YXJlIGFuZCBhc3NvY2lhdGVkIGRvY3VtZW50YXRpb24gZmlsZXMgKHRoZSAiU29mdHdhcmUiKSwg'
    'dG8gZGVhbAppbiB0aGUgU29mdHdhcmUgd2l0aG91dCByZXN0cmljdGlvbiwgaW5jbHVkaW5nIHdp'
    'dGhvdXQgbGltaXRhdGlvbiB0aGUgcmlnaHRzCnRvIHVzZSwgY29weSwgbW9kaWZ5LCBtZXJnZSwg'
    'cHVibGlzaCwgZGlzdHJpYnV0ZSwgc3VibGljZW5zZSwgYW5kL29yIHNlbGwKY29waWVzIG9mIHRo'
    'ZSBTb2Z0d2FyZSwgYW5kIHRvIHBlcm1pdCBwZXJzb25zIHRvIHdob20gdGhlIFNvZnR3YXJlIGlz'
    'CmZ1cm5pc2hlZCB0byBkbyBzbywgc3ViamVjdCB0byB0aGUgZm9sbG93aW5nIGNvbmRpdGlvbnM6'
    'CgpUaGUgYWJvdmUgY29weXJpZ2h0IG5vdGljZSBhbmQgdGhpcyBwZXJtaXNzaW9uIG5vdGljZSBz'
    'aGFsbCBiZSBpbmNsdWRlZCBpbiBhbGwKY29waWVzIG9yIHN1YnN0YW50aWFsIHBvcnRpb25zIG9m'
    'IHRoZSBTb2Z0d2FyZS4KClRIRSBTT0ZUV0FSRSBJUyBQUk9WSURFRCAiQVMgSVMiLCBXSVRIT1VU'
    'IFdBUlJBTlRZIE9GIEFOWSBLSU5ELCBFWFBSRVNTIE9SCklNUExJRUQsIElOQ0xVRElORyBCVVQg'
    'Tk9UIExJTUlURUQgVE8gVEhFIFdBUlJBTlRJRVMgT0YgTUVSQ0hBTlRBQklMSVRZLApGSVRORVNT'
    'IEZPUiBBIFBBUlRJQ1VMQVIgUFVSUE9TRSBBTkQgTk9OSU5GUklOR0VNRU5ULiBJTiBOTyBFVkVO'
    'VCBTSEFMTCBUSEUKQVVUSE9SUyBPUiBDT1BZUklHSFQgSE9MREVSUyBCRSBMSUFCTEUgRk9SIEFO'
    'WSBDTEFJTSwgREFNQUdFUyBPUiBPVEhFUgpMSUFCSUxJVFksIFdIRVRIRVIgSU4gQU4gQUNUSU9O'
    'IE9GIENPTlRSQUNULCBUT1JUIE9SIE9USEVSV0lTRSwgQVJJU0lORyBGUk9NLApPVVQgT0YgT1Ig'
    'SU4gQ09OTkVDVElPTiBXSVRIIFRIRSBTT0ZUV0FSRSBPUiBUSEUgVVNFIE9SIE9USEVSIERFQUxJ'
    'TkdTIElOIFRIRQpTT0ZUV0FSRS4KCgoKPT09PT0gQnVuZGxlZCBtb2RpZmllZCBsZXN0IHRlc3Qg'
    'ZnJhbWV3b3JrOiBvcmlnaW5hbCBub3RpY2UgPT09PT0KLy8gQ29weXJpZ2h0IDIwMTMtMjAxOCBi'
    'eSBNYXJ0aW4gTW9lbmUKLy8KLy8gbGVzdCBpcyBiYXNlZCBvbiBpZGVhcyBieSBLZXZsaW4gSGVu'
    'bmV5LCBzZWUgdmlkZW8gYXQKLy8gaHR0cDovL3NraWxsc21hdHRlci5jb20vcG9kY2FzdC9hZ2ls'
    'ZS10ZXN0aW5nL2tldmxpbi1oZW5uZXktcmV0aGlua2luZy11bml0LXRlc3RpbmctaW4tYy1wbHVz'
    'LXBsdXMKLy8KLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIEJvb3N0IFNvZnR3YXJlIExpY2Vuc2Us'
    'IFZlcnNpb24gMS4wLiAoU2VlIGFjY29tcGFueWluZwovLyBmaWxlIExJQ0VOU0UudHh0IG9yIGNv'
    'cHkgYXQgaHR0cDovL3d3dy5ib29zdC5vcmcvTElDRU5TRV8xXzAudHh0KQoKPT09PT0gQlNMLTEu'
    'MCBmdWxsIHN0YW5kYXJkIHRlcm1zID09PT09CkJvb3N0IFNvZnR3YXJlIExpY2Vuc2UgLSBWZXJz'
    'aW9uIDEuMCAtIEF1Z3VzdCAxN3RoLCAyMDAzCgpQZXJtaXNzaW9uIGlzIGhlcmVieSBncmFudGVk'
    'LCBmcmVlIG9mIGNoYXJnZSwgdG8gYW55IHBlcnNvbiBvciBvcmdhbml6YXRpb24gb2J0YWluaW5n'
    'IGEgY29weSBvZiB0aGUgc29mdHdhcmUgYW5kIGFjY29tcGFueWluZyBkb2N1bWVudGF0aW9uIGNv'
    'dmVyZWQgYnkgdGhpcyBsaWNlbnNlICh0aGUgIlNvZnR3YXJlIikgdG8gdXNlLCByZXByb2R1Y2Us'
    'IGRpc3BsYXksIGRpc3RyaWJ1dGUsIGV4ZWN1dGUsIGFuZCB0cmFuc21pdCB0aGUgU29mdHdhcmUs'
    'IGFuZCB0byBwcmVwYXJlIGRlcml2YXRpdmUgd29ya3Mgb2YgdGhlIFNvZnR3YXJlLCBhbmQgdG8g'
    'cGVybWl0IHRoaXJkLXBhcnRpZXMgdG8gd2hvbSB0aGUgU29mdHdhcmUgaXMgZnVybmlzaGVkIHRv'
    'IGRvIHNvLCBhbGwgc3ViamVjdCB0byB0aGUgZm9sbG93aW5nOgoKVGhlIGNvcHlyaWdodCBub3Rp'
    'Y2VzIGluIHRoZSBTb2Z0d2FyZSBhbmQgdGhpcyBlbnRpcmUgc3RhdGVtZW50LCBpbmNsdWRpbmcg'
    'dGhlIGFib3ZlIGxpY2Vuc2UgZ3JhbnQsIHRoaXMgcmVzdHJpY3Rpb24gYW5kIHRoZSBmb2xsb3dp'
    'bmcgZGlzY2xhaW1lciwgbXVzdCBiZSBpbmNsdWRlZCBpbiBhbGwgY29waWVzIG9mIHRoZSBTb2Z0'
    'd2FyZSwgaW4gd2hvbGUgb3IgaW4gcGFydCwgYW5kIGFsbCBkZXJpdmF0aXZlIHdvcmtzIG9mIHRo'
    'ZSBTb2Z0d2FyZSwgdW5sZXNzIHN1Y2ggY29waWVzIG9yIGRlcml2YXRpdmUgd29ya3MgYXJlIHNv'
    'bGVseSBpbiB0aGUgZm9ybSBvZiBtYWNoaW5lLWV4ZWN1dGFibGUgb2JqZWN0IGNvZGUgZ2VuZXJh'
    'dGVkIGJ5IGEgc291cmNlIGxhbmd1YWdlIHByb2Nlc3Nvci4KClRIRSBTT0ZUV0FSRSBJUyBQUk9W'
    'SURFRCAiQVMgSVMiLCBXSVRIT1VUIFdBUlJBTlRZIE9GIEFOWSBLSU5ELCBFWFBSRVNTIE9SIElN'
    'UExJRUQsIElOQ0xVRElORyBCVVQgTk9UIExJTUlURUQgVE8gVEhFIFdBUlJBTlRJRVMgT0YgTUVS'
    'Q0hBTlRBQklMSVRZLCBGSVRORVNTIEZPUiBBIFBBUlRJQ1VMQVIgUFVSUE9TRSwgVElUTEUgQU5E'
    'IE5PTi1JTkZSSU5HRU1FTlQuIElOIE5PIEVWRU5UIFNIQUxMIFRIRSBDT1BZUklHSFQgSE9MREVS'
    'UyBPUiBBTllPTkUgRElTVFJJQlVUSU5HIFRIRSBTT0ZUV0FSRSBCRSBMSUFCTEUgRk9SIEFOWSBE'
    'QU1BR0VTIE9SIE9USEVSIExJQUJJTElUWSwgV0hFVEhFUiBJTiBDT05UUkFDVCwgVE9SVCBPUiBP'
    'VEhFUldJU0UsIEFSSVNJTkcgRlJPTSwgT1VUIE9GIE9SIElOIENPTk5FQ1RJT04gV0lUSCBUSEUg'
    'U09GVFdBUkUgT1IgVEhFIFVTRSBPUiBPVEhFUiBERUFMSU5HUyBJTiBUSEUgU09GVFdBUkUuCgoK'
    'PT09PT0gQnVuZGxlZCBDTWFrZSBoZWxwZXI6IG9yaWdpbmFsIFNQRFggY29weXJpZ2h0L2xpY2Vu'
    'c2Ugbm90aWNlID09PT09CiMgU1BEWC1GaWxlQ29weXJpZ2h0VGV4dDogMjAxMi0yMDIxIElzdGl0'
    'dXRvIEl0YWxpYW5vIGRpIFRlY25vbG9naWEgKElJVCkKIyBTUERYLUxpY2Vuc2UtSWRlbnRpZmll'
    'cjogQlNELTMtQ2xhdXNlCgo9PT09PSBCU0QtMy1DbGF1c2UgZnVsbCBzdGFuZGFyZCB0ZXJtcywg'
    'cGxhY2Vob2xkZXJzIG5vdCBwcm9qZWN0IGhvbGRlcnMgPT09PT0KQ29weXJpZ2h0IChjKSA8eWVh'
    'cj4gPG93bmVyPi4gCgpSZWRpc3RyaWJ1dGlvbiBhbmQgdXNlIGluIHNvdXJjZSBhbmQgYmluYXJ5'
    'IGZvcm1zLCB3aXRoIG9yIHdpdGhvdXQgbW9kaWZpY2F0aW9uLCBhcmUgcGVybWl0dGVkIHByb3Zp'
    'ZGVkIHRoYXQgdGhlIGZvbGxvd2luZyBjb25kaXRpb25zIGFyZSBtZXQ6CgoxLiBSZWRpc3RyaWJ1'
    'dGlvbnMgb2Ygc291cmNlIGNvZGUgbXVzdCByZXRhaW4gdGhlIGFib3ZlIGNvcHlyaWdodCBub3Rp'
    'Y2UsIHRoaXMgbGlzdCBvZiBjb25kaXRpb25zIGFuZCB0aGUgZm9sbG93aW5nIGRpc2NsYWltZXIu'
    'CgoyLiBSZWRpc3RyaWJ1dGlvbnMgaW4gYmluYXJ5IGZvcm0gbXVzdCByZXByb2R1Y2UgdGhlIGFi'
    'b3ZlIGNvcHlyaWdodCBub3RpY2UsIHRoaXMgbGlzdCBvZiBjb25kaXRpb25zIGFuZCB0aGUgZm9s'
    'bG93aW5nIGRpc2NsYWltZXIgaW4gdGhlIGRvY3VtZW50YXRpb24gYW5kL29yIG90aGVyIG1hdGVy'
    'aWFscyBwcm92aWRlZCB3aXRoIHRoZSBkaXN0cmlidXRpb24uCgozLiBOZWl0aGVyIHRoZSBuYW1l'
    'IG9mIHRoZSBjb3B5cmlnaHQgaG9sZGVyIG5vciB0aGUgbmFtZXMgb2YgaXRzIGNvbnRyaWJ1dG9y'
    'cyBtYXkgYmUgdXNlZCB0byBlbmRvcnNlIG9yIHByb21vdGUgcHJvZHVjdHMgZGVyaXZlZCBmcm9t'
    'IHRoaXMgc29mdHdhcmUgd2l0aG91dCBzcGVjaWZpYyBwcmlvciB3cml0dGVuIHBlcm1pc3Npb24u'
    'CgpUSElTIFNPRlRXQVJFIElTIFBST1ZJREVEIEJZIFRIRSBDT1BZUklHSFQgSE9MREVSUyBBTkQg'
    'Q09OVFJJQlVUT1JTICJBUyBJUyIgQU5EIEFOWSBFWFBSRVNTIE9SIElNUExJRUQgV0FSUkFOVElF'
    'UywgSU5DTFVESU5HLCBCVVQgTk9UIExJTUlURUQgVE8sIFRIRSBJTVBMSUVEIFdBUlJBTlRJRVMg'
    'T0YgTUVSQ0hBTlRBQklMSVRZIEFORCBGSVRORVNTIEZPUiBBIFBBUlRJQ1VMQVIgUFVSUE9TRSBB'
    'UkUgRElTQ0xBSU1FRC4gSU4gTk8gRVZFTlQgU0hBTEwgVEhFIENPUFlSSUdIVCBIT0xERVIgT1Ig'
    'Q09OVFJJQlVUT1JTIEJFIExJQUJMRSBGT1IgQU5ZIERJUkVDVCwgSU5ESVJFQ1QsIElOQ0lERU5U'
    'QUwsIFNQRUNJQUwsIEVYRU1QTEFSWSwgT1IgQ09OU0VRVUVOVElBTCBEQU1BR0VTIChJTkNMVURJ'
    'TkcsIEJVVCBOT1QgTElNSVRFRCBUTywgUFJPQ1VSRU1FTlQgT0YgU1VCU1RJVFVURSBHT09EUyBP'
    'UiBTRVJWSUNFUzsgTE9TUyBPRiBVU0UsIERBVEEsIE9SIFBST0ZJVFM7IE9SIEJVU0lORVNTIElO'
    'VEVSUlVQVElPTikgSE9XRVZFUiBDQVVTRUQgQU5EIE9OIEFOWSBUSEVPUlkgT0YgTElBQklMSVRZ'
    'LCBXSEVUSEVSIElOIENPTlRSQUNULCBTVFJJQ1QgTElBQklMSVRZLCBPUiBUT1JUIChJTkNMVURJ'
    'TkcgTkVHTElHRU5DRSBPUiBPVEhFUldJU0UpIEFSSVNJTkcgSU4gQU5ZIFdBWSBPVVQgT0YgVEhF'
    'IFVTRSBPRiBUSElTIFNPRlRXQVJFLCBFVkVOIElGIEFEVklTRUQgT0YgVEhFIFBPU1NJQklMSVRZ'
    'IE9GIFNVQ0ggREFNQUdFLgoKCj09PT09IEJ1bmRsZWQgQ1BNIGV4YW1wbGU6IG9yaWdpbmFsIGZ1'
    'bGwgTUlUIGdyYW50ID09PT09CiMgQ1BNLmNtYWtlIC0gQ01ha2UncyBtaXNzaW5nIHBhY2thZ2Ug'
    'bWFuYWdlcgojID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0KIyBT'
    'ZWUgaHR0cHM6Ly9naXRodWIuY29tL2NwbS1jbWFrZS9DUE0uY21ha2UgZm9yIHVzYWdlIGFuZCB1'
    'cGRhdGUgaW5zdHJ1Y3Rpb25zLgojCiMgTUlUIExpY2Vuc2UKIyAtLS0tLS0tLS0tLQojW1sKICBD'
    'b3B5cmlnaHQgKGMpIDIwMTktMjAyMyBMYXJzIE1lbGNoaW9yIGFuZCBjb250cmlidXRvcnMKCiAg'
    'UGVybWlzc2lvbiBpcyBoZXJlYnkgZ3JhbnRlZCwgZnJlZSBvZiBjaGFyZ2UsIHRvIGFueSBwZXJz'
    'b24gb2J0YWluaW5nIGEgY29weQogIG9mIHRoaXMgc29mdHdhcmUgYW5kIGFzc29jaWF0ZWQgZG9j'
    'dW1lbnRhdGlvbiBmaWxlcyAodGhlICJTb2Z0d2FyZSIpLCB0byBkZWFsCiAgaW4gdGhlIFNvZnR3'
    'YXJlIHdpdGhvdXQgcmVzdHJpY3Rpb24sIGluY2x1ZGluZyB3aXRob3V0IGxpbWl0YXRpb24gdGhl'
    'IHJpZ2h0cwogIHRvIHVzZSwgY29weSwgbW9kaWZ5LCBtZXJnZSwgcHVibGlzaCwgZGlzdHJpYnV0'
    'ZSwgc3VibGljZW5zZSwgYW5kL29yIHNlbGwKICBjb3BpZXMgb2YgdGhlIFNvZnR3YXJlLCBhbmQg'
    'dG8gcGVybWl0IHBlcnNvbnMgdG8gd2hvbSB0aGUgU29mdHdhcmUgaXMKICBmdXJuaXNoZWQgdG8g'
    'ZG8gc28sIHN1YmplY3QgdG8gdGhlIGZvbGxvd2luZyBjb25kaXRpb25zOgoKICBUaGUgYWJvdmUg'
    'Y29weXJpZ2h0IG5vdGljZSBhbmQgdGhpcyBwZXJtaXNzaW9uIG5vdGljZSBzaGFsbCBiZSBpbmNs'
    'dWRlZCBpbiBhbGwKICBjb3BpZXMgb3Igc3Vic3RhbnRpYWwgcG9ydGlvbnMgb2YgdGhlIFNvZnR3'
    'YXJlLgoKICBUSEUgU09GVFdBUkUgSVMgUFJPVklERUQgIkFTIElTIiwgV0lUSE9VVCBXQVJSQU5U'
    'WSBPRiBBTlkgS0lORCwgRVhQUkVTUyBPUgogIElNUExJRUQsIElOQ0xVRElORyBCVVQgTk9UIExJ'
    'TUlURUQgVE8gVEhFIFdBUlJBTlRJRVMgT0YgTUVSQ0hBTlRBQklMSVRZLAogIEZJVE5FU1MgRk9S'
    'IEEgUEFSVElDVUxBUiBQVVJQT1NFIEFORCBOT05JTkZSSU5HRU1FTlQuIElOIE5PIEVWRU5UIFNI'
    'QUxMIFRIRQogIEFVVEhPUlMgT1IgQ09QWVJJR0hUIEhPTERFUlMgQkUgTElBQkxFIEZPUiBBTlkg'
    'Q0xBSU0sIERBTUFHRVMgT1IgT1RIRVIKICBMSUFCSUxJVFksIFdIRVRIRVIgSU4gQU4gQUNUSU9O'
    'IE9GIENPTlRSQUNULCBUT1JUIE9SIE9USEVSV0lTRSwgQVJJU0lORyBGUk9NLAogIE9VVCBPRiBP'
    'UiBJTiBDT05ORUNUSU9OIFdJVEggVEhFIFNPRlRXQVJFIE9SIFRIRSBVU0UgT1IgT1RIRVIgREVB'
    'TElOR1MgSU4gVEhFCiAgU09GVFdBUkUuCl1dCg=='
)
decoded=base64.b64decode(encoded,validate=True)
assert len(decoded)==6697 and hashlib.sha256(decoded).hexdigest()=='e4330675c2cb4ddba5eacabaedc2e9b4ac49c5c750ffc0e6a904e72c2ba9897b'
pathlib.Path('.packaging-qa/NOTICES-and-LICENSES.txt').write_bytes(decoded)
GSL_FULL_LICENSE_BUNDLE_B64

python3 - <<'GSL_OWNED_MANIFEST'
import hashlib,json,pathlib
q=pathlib.Path('.packaging-qa')
names=['consumer.cpp','peer.cpp','CMakeLists.txt','run-installed.py','upstream-audit.py','test-registry.json','original-source-manifest.json','NOTICES-and-LICENSES.txt','Apache-2.0.txt','BSL-1.0.txt','BSD-3-Clause.txt']
(q/'owned-files.json').write_text(json.dumps({name:dict(sha256=hashlib.sha256((q/name).read_bytes()).hexdigest(),bytes=(q/name).stat().st_size) for name in names},sort_keys=True)+'\n')
GSL_OWNED_MANIFEST

%build
export CXXFLAGS="%{optflags}"
export LDFLAGS="%{?build_ldflags}"
cmake -S . -B .packaging-build/default -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_INCLUDEDIR:PATH=include -DCMAKE_INSTALL_DATADIR:PATH=share -DCMAKE_EXPORT_PACKAGE_REGISTRY=OFF
cmake --build .packaging-build/default --parallel 2
cmake -S . -B .packaging-build/tests -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_INCLUDEDIR:PATH=include -DCMAKE_INSTALL_DATADIR:PATH=share -DCMAKE_EXPORT_PACKAGE_REGISTRY=OFF -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DGSL_LITE_OPT_BUILD_TESTS=ON
cmake --build .packaging-build/tests --parallel 2

%install
DESTDIR=%{buildroot} cmake --install .packaging-build/default
install -d %{buildroot}%{_libexecdir}/gsl-lite/qa %{buildroot}%{_licensedir}/gsl-lite
cp -a .packaging-qa/. %{buildroot}%{_libexecdir}/gsl-lite/qa/
install -m 0644 LICENSE %{buildroot}%{_licensedir}/gsl-lite/LICENSE.MIT
install -m 0644 .packaging-qa/Apache-2.0.txt .packaging-qa/BSL-1.0.txt .packaging-qa/BSD-3-Clause.txt .packaging-qa/NOTICES-and-LICENSES.txt %{buildroot}%{_licensedir}/gsl-lite/
cp -a .packaging-qa/source-notices %{buildroot}%{_licensedir}/gsl-lite/

%check
export LC_ALL=C LANG=C
python3 - <<'GSL_PRODUCTION_DEFAULTS'
import pathlib
def cache(path):
    return dict(line.split('=',1) for line in pathlib.Path(path).read_text().splitlines() if '=' in line and not line.startswith(('#','//')))
p=cache('.packaging-build/default/CMakeCache.txt');t=cache('.packaging-build/tests/CMakeCache.txt')
keys=['GSL_LITE_OPT_BUILD_TESTS','GSL_LITE_OPT_BUILD_CUDA_TESTS','GSL_LITE_OPT_BUILD_EXAMPLES','GSL_LITE_OPT_BUILD_STATIC_ANALYSIS_DEMOS']
assert all(p[k+':BOOL']=='OFF' for k in keys)
assert t['GSL_LITE_OPT_BUILD_TESTS:BOOL']=='ON' and all(t[k+':BOOL']=='OFF' for k in keys[1:])
assert p['CMAKE_INSTALL_INCLUDEDIR:PATH']=='include' and t['CMAKE_INSTALL_INCLUDEDIR:PATH']=='include'
print('GSL_LITE_PRODUCTION_DEFAULTS_RETAINED_SEPARATE_ORIGINAL_TEST_OPT_IN')
GSL_PRODUCTION_DEFAULTS
python3 .packaging-qa/upstream-audit.py
python3 %{buildroot}%{_libexecdir}/gsl-lite/qa/run-installed.py --prefix %{buildroot}%{_prefix} --work-dir .packaging-build/buildroot-installed-qa
python3 - <<'GSL_ORIGINAL_AFTER_QA'
import hashlib,json,pathlib
m=json.loads(pathlib.Path('.packaging-qa/original-source-manifest.json').read_bytes());assert len(m)==55
for name,row in m.items():
    p=pathlib.Path(name);b=p.read_bytes()
    assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'] and p.stat().st_mode&0o777==row['extracted_mode']
print('GSL_LITE_ALL_55_ORIGINAL_FILES_UNCHANGED_AFTER_QA')
GSL_ORIGINAL_AFTER_QA

%files
%license %{_licensedir}/gsl-lite
%doc README.md CHANGES.txt doc/Reference.md
%{_includedir}/gsl-lite/
%{_includedir}/gsl/gsl-lite.hpp
%{_datadir}/cmake/gsl-lite/
%{_libexecdir}/gsl-lite/

%changelog
* Wed Oct 28 2026 openEuler package contributors - 1.1.1-1
- Preserve original production defaults, complete GNU14 test matrix and all55 notices
- Add installed/relocated multi-TU consumers for every imported target and alias
