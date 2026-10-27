# SPDX-License-Identifier: Apache-2.0
Name:           libsubprocess
Version:        2.5
Release:        1%{?dist}
Summary:        Header-only C++11 process and pipe library
License:        MIT AND Apache-2.0
URL:            https://github.com/arun11299/cpp-subprocess
Source0:        libsubprocess-v2.5.tar.gz
Source1:        Apache-2.0.txt
Patch0:         0001-repair-export-and-bound-process-I-O.patch
Patch1:         0002-use-canonical-cmake-version-file-name.patch
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  cmake >= 3.23
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
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
Requires:       cmake >= 3.23
Requires:       coreutils
Requires:       diffutils
Requires:       gcc-c++
Requires:       glibc-devel
Requires:       grep
Requires:       make

%description
A header-only C++11 library for POSIX process creation, pipes, redirection and
exit status handling. Preserve the original ten CTest programs with assertions
enabled, and add bounded process-I/O and installed CMake/header regressions.
No DSO, static archive or command-line program is invented. The source's two
prebuilt Mach-O artifacts are retained as source/notices only and never executed.
Target tests do not establish universal process safety or Windows behavior.

%prep
%setup -q -n arun11299-cpp-subprocess-60d4ad8
find . -type f -print | LC_ALL=C sort > ../libsubprocess-original-files.list
test "$(wc -l < ../libsubprocess-original-files.list)" -eq 27
mkdir source-notices
while IFS= read -r item; do
    rel="${item#./}"
    destination="source-notices/$rel.notice"
    install -d "${destination%/*}"
    cp -p "$item" "$destination"
    chmod 0644 "$destination"
done < ../libsubprocess-original-files.list
(cd source-notices; find . -type f -name '*.notice' -print | LC_ALL=C sort | while IFS= read -r item; do sha256sum "$item"; done) > ../libsubprocess-original-SHA256SUMS
mv ../libsubprocess-original-SHA256SUMS source-notices/SHA256SUMS
test "$(wc -l < source-notices/SHA256SUMS)" -eq 27
%autopatch -p1
cp -p %{SOURCE1} Apache-2.0.txt
cat > regressions.cpp <<'LIBSUBPROCESS_CPP'
// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 openEuler supplementary packaging contributors.
// Additive target-only regressions. No upstream test is replaced.
#include <cpp-subprocess/subprocess.hpp>
#include <cerrno>
#include <cstdio>
#include <cstring>
#include <initializer_list>
#include <stdexcept>
#include <string>
#include <vector>
#include <unistd.h>
#ifdef NDEBUG
#error "All original and owned assertions must remain enabled"
#endif
namespace sp = subprocess;
static void need(bool condition, const char* message) {
  if (!condition) throw std::runtime_error(message);
}
static std::string data(const sp::Buffer& b) {
  need(b.length <= b.buf.size(), "buffer length exceeds actual vector");
  return std::string(b.buf.begin(), b.buf.begin() + b.length);
}
static std::string large_error() { return std::string(65536, 'Z') + "\n"; }
static int emit(const std::string& mode) {
  if (mode == "emit-out") {
    const char text[] = "owned stdout\n";
    return std::fwrite(text, 1, sizeof(text)-1, stdout) == sizeof(text)-1 ? 0 : 90;
  }
  if (mode == "emit-err") {
    const std::string text = large_error();
    return std::fwrite(text.data(), 1, text.size(), stderr) == text.size() ? 0 : 91;
  }
  if (mode == "emit-both") {
    const char out[] = "owned out\n", err[] = "owned err\n";
    if (std::fwrite(out, 1, sizeof(out)-1, stdout) != sizeof(out)-1) return 92;
    if (std::fwrite(err, 1, sizeof(err)-1, stderr) != sizeof(err)-1) return 93;
    return 7;
  }
  return 94;
}
int main(int argc, char** argv) {
  try {
    need(argc >= 1 && argv[0] && argv[0][0] == '/', "caller must supply absolute self executable");
    const std::string self = argv[0];
    if (argc == 2 && std::string(argv[1]).compare(0, 5, "emit-") == 0) return emit(argv[1]);
    if (argc == 2 && std::string(argv[1]) == "default-redirection-helper") {
      sp::Popen child(std::vector<std::string>{self, "emit-err"}, sp::error{sp::STDOUT});
      return child.wait() == 0 ? 0 : 95;
    }
    need(argc == 1, "unknown owned helper mode");
    need(sp::util::join({}).empty(), "empty join");
    need(sp::util::join({"a", "b"}, "::") == "a::b", "multi-byte separator");
    need(sp::util::join({"a", "b"}, "") == "ab", "empty separator");
    need(sp::util::join({"a"}, "::") == "a", "singleton join");
    std::puts("case01-join PASS");
    unsigned invalid = 0;
    try { sp::Popen p(std::vector<std::string>{}); }
    catch (const std::invalid_argument& e) {
      need(std::string(e.what()) == "subprocess command must not be empty", "empty vector diagnostic"); ++invalid;
    }
    try { sp::Popen p(std::initializer_list<const char*>{}); }
    catch (const std::invalid_argument& e) {
      need(std::string(e.what()) == "subprocess command must not be empty", "empty list diagnostic"); ++invalid;
    }
    need(invalid == 2, "both empty command forms must reject before fork");
    std::puts("case02-empty-command PASS");
    {
      sp::Popen p(std::vector<std::string>{self, "emit-out"}, sp::output{sp::PIPE});
      const auto out = p.communicate();
      need(data(out.first) == "owned stdout\n" && data(out.second).empty() && p.retcode() == 0, "stdout exact bytes/status");
    }
    std::puts("case03-stdout PASS");
    {
      sp::Popen p(std::vector<std::string>{self, "emit-err"}, sp::error{sp::PIPE});
      const auto out = p.communicate();
      need(data(out.first).empty() && data(out.second) == large_error() && p.retcode() == 0, "large stderr-only exact bytes/status");
    }
    std::puts("case04-large-stderr PASS");
    {
      sp::Popen p(std::vector<std::string>{self, "emit-both"}, sp::output{sp::PIPE}, sp::error{sp::PIPE});
      const auto out = p.communicate();
      need(data(out.first) == "owned out\n" && data(out.second) == "owned err\n" && p.retcode() == 7, "two-pipe bytes and nonzero status");
    }
    std::puts("case05-two-pipe-status PASS");
    for (const char* mode : {"emit-err", "default-redirection-helper"}) {
      sp::Popen p = std::string(mode) == "emit-err"
        ? sp::Popen(std::vector<std::string>{self, mode}, sp::output{sp::PIPE}, sp::error{sp::STDOUT})
        : sp::Popen(std::vector<std::string>{self, mode}, sp::output{sp::PIPE}, sp::error{sp::PIPE});
      const auto out = p.communicate();
      need(data(out.first) == large_error() && data(out.second).empty() && p.retcode() == 0, "stderr merged into explicit/default stdout");
    }
    std::puts("case06-stderr-redirection PASS");
    {
      bool caught = false;
      try {
        sp::Popen p(std::vector<std::string>{self, "emit-out"}, sp::preexec_func{[] {
          throw sp::OSError(std::string(2048, 'L'), EINVAL);
        }});
      } catch (const sp::CalledProcessError& e) {
        need(e.retcode == 1 && std::string(e.what()) == std::string(sp::SP_MAX_ERR_BUF_SIZ, 'L'), "length-bound startup failure");
        caught = true;
      }
      need(caught, "long startup failure must throw");
    }
    std::puts("case07-startup-error-bound PASS");
    {
      sp::Popen p(std::vector<std::string>{self, "emit-both"}, sp::output{sp::PIPE}, sp::error{sp::PIPE});
      need(::close(::fileno(p.output())) == 0, "close only owned output read descriptor");
      bool caught = false;
      try { p.communicate(); }
      catch (const sp::OSError& e) {
        need(std::string(e.what()) == std::string("read to obuf failed: ") + std::strerror(EBADF), "threaded read failure must propagate EBADF");
        caught = true;
      }
      p.wait(); // Reap this owned child even when communication throws.
      need(caught, "threaded read failure silently became empty output");
    }
    std::puts("case08-threaded-error PASS");
    {
      sp::Popen p(std::vector<std::string>{self, "emit-out"}, sp::output{sp::PIPE});
      std::vector<char> bytes;
      const int count = sp::util::read_all(p.output(), bytes);
      need(count == 13 && std::string(bytes.begin(), bytes.end()) == "owned stdout\n", "empty destination must grow and read exact data");
      p.close_output(); need(p.wait() == 0, "empty-buffer child status");
    }
    std::puts("case09-empty-buffer PASS");
    {
      std::vector<sp::Popen> children;
      for (int i = 0; i < 3; ++i) {
        children.emplace_back(sp::Popen(std::vector<std::string>{self, "emit-out"}, sp::output{sp::PIPE}));
      }
      for (auto& child : children) {
        const auto out = child.communicate();
        need(data(out.first) == "owned stdout\n" && out.second.length == 0 && child.retcode() == 0,
             "moved stream must address its destination, not former temporary/vector storage");
      }
    }
    std::puts("case10-moved-stream PASS");
    return 0;
  } catch (const std::exception& e) {
    std::fprintf(stderr, "owned-regression failure: %%s\n", e.what()); return 1;
  }
}

LIBSUBPROCESS_CPP
cat > run-qa.sh <<'LIBSUBPROCESS_QA'
#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 openEuler supplementary packaging contributors.
set -euo pipefail
export LC_ALL=C LANG=C PATH=/usr/bin:/bin
unset LD_PRELOAD LD_LIBRARY_PATH
test "$#" -eq 1
prefix=$(readlink -f -- "$1")
test -f "$prefix/include/cpp-subprocess/subprocess.hpp"
qa="$prefix/share/libsubprocess-tests"
test -f "$prefix/lib64/cmake/subprocess/subprocess-config.cmake"
(cd "$qa"; sha256sum -c SHA256SUMS)
before=$(sha256sum "$qa/regressions.cpp" "$qa/run-qa.sh" "$prefix/include/cpp-subprocess/subprocess.hpp")
work=$(mktemp -d /tmp/libsubprocess-qa.XXXXXXXX)
case "$work" in /tmp/libsubprocess-qa.*) ;; *) exit 80;; esac
trap 'rm -rf -- "$work"' EXIT
cp "$qa/regressions.cpp" "$work/regressions.cpp"
cat > "$work/CMakeLists.txt" <<'OWNED_CMAKE'
cmake_minimum_required(VERSION 3.23)
project(libsubprocess_owned_consumer LANGUAGES CXX)
find_package(subprocess 2.5 EXACT CONFIG REQUIRED
  PATHS "${LIBSUBPROCESS_PREFIX}/lib64/cmake/subprocess" NO_DEFAULT_PATH)
add_executable(owned-consumer regressions.cpp)
target_link_libraries(owned-consumer PRIVATE cpp-subprocess::subprocess)
target_compile_features(owned-consumer PRIVATE cxx_std_11)
target_compile_options(owned-consumer PRIVATE -H -UNDEBUG)
OWNED_CMAKE
cmake -S "$work" -B "$work/build" \
  -DLIBSUBPROCESS_PREFIX="$prefix" -DCMAKE_CXX_COMPILER=/usr/bin/g++ \
  -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_FLAGS="${CXXFLAGS:--O2 -g}" \
  -DCMAKE_EXE_LINKER_FLAGS="${LDFLAGS:-}" -DCMAKE_CXX_FLAGS_DEBUG="-g -UNDEBUG" \
  -DCMAKE_FIND_USE_PACKAGE_REGISTRY=OFF -DCMAKE_FIND_PACKAGE_NO_PACKAGE_REGISTRY=ON
cmake --build "$work/build" --verbose > "$work/compile.log" 2>&1
cat "$work/compile.log"
grep -F -- "$prefix/include/cpp-subprocess/subprocess.hpp" "$work/compile.log"
program="$work/build/owned-consumer"
test -x "$program"
readelf -h "$program" > "$work/header.txt"; cat "$work/header.txt"
grep -Eq 'Class:[[:space:]]+ELF64' "$work/header.txt"
grep -Eq 'Machine:[[:space:]]+RISC-V' "$work/header.txt"
readelf -d "$program" > "$work/dynamic.txt"; cat "$work/dynamic.txt"
if grep -Eq '\((RPATH|RUNPATH)\)' "$work/dynamic.txt"; then exit 81; fi
program_before=$(sha256sum "$program")
status=0
timeout 30 "$program" > "$work/actual.stdout" 2> "$work/actual.stderr" || status=$?
cat "$work/actual.stdout"
cat "$work/actual.stderr" >&2
test "$status" -eq 0
test ! -s "$work/actual.stderr"
cmp "$qa/expected.stdout" "$work/actual.stdout"
test "$(sha256sum "$program")" = "$program_before"
test "$(sha256sum "$qa/regressions.cpp" "$qa/run-qa.sh" "$prefix/include/cpp-subprocess/subprocess.hpp")" = "$before"
printf '%%s\n' "LIBSUBPROCESS-OWNED-CONSUMER: 10 exact groups passed; temporary target ELF checked, not retained as installed product."
printf '%%s\n' "$program_before" "$before"

LIBSUBPROCESS_QA
cat > expected.stdout <<'LIBSUBPROCESS_EXPECTED'
case01-join PASS
case02-empty-command PASS
case03-stdout PASS
case04-large-stderr PASS
case05-two-pipe-status PASS
case06-stderr-redirection PASS
case07-startup-error-bound PASS
case08-threaded-error PASS
case09-empty-buffer PASS
case10-moved-stream PASS
LIBSUBPROCESS_EXPECTED
sha256sum regressions.cpp run-qa.sh expected.stdout > SHA256SUMS

%build
%set_build_flags
cmake -S . -B build \
    -DCMAKE_CXX_COMPILER=/usr/bin/g++ \
    -DCMAKE_CXX_FLAGS="$CXXFLAGS" \
    -DCMAKE_EXE_LINKER_FLAGS="$LDFLAGS" \
    -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_FLAGS_DEBUG="-g -UNDEBUG" \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DSUBPROCESS_INSTALL=ON -DSUBPROCESS_TESTS=ON -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
cmake --build build --parallel %{_smp_build_ncpus} --verbose

%install
DESTDIR=%{buildroot} cmake --install build
install -d %{buildroot}%{_datadir}/libsubprocess-tests
install -m 0644 regressions.cpp run-qa.sh expected.stdout SHA256SUMS %{buildroot}%{_datadir}/libsubprocess-tests/

%check
export LC_ALL=C LANG=C
ctest --test-dir build --show-only=json-v1 > ctest-registered.json
python3 - <<'LIBSUBPROCESS_CTEST'
import json
from pathlib import Path
tests=json.loads(Path('ctest-registered.json').read_text())['tests']
expected={'test_subprocess','test_cat','test_double_quotes','test_env','test_err_redirection','test_exception','test_split','test_main','test_ret_code','test_redirection'}
assert len(tests)==10 and {t['name'] for t in tests}==expected
commands=json.loads(Path('build/compile_commands.json').read_text())
assert len(commands)==10 and all('-UNDEBUG' in row['command'] and '-DNDEBUG' not in row['command'] for row in commands)
print('LIBSUBPROCESS-ORIGINAL-REGISTRATION: 10 CTests; assertions not disabled; weaker demonstrational bodies remain disclosed.')
LIBSUBPROCESS_CTEST
ctest --test-dir build --verbose --output-on-failure --timeout 30 --parallel 1
bash run-qa.sh %{buildroot}%{_prefix}

%files
%license LICENSE.MIT Apache-2.0.txt source-notices
%doc README.md
%{_includedir}/cpp-subprocess/
%{_libdir}/cmake/subprocess/
%{_datadir}/libsubprocess-tests/

%changelog
* Tue Oct 27 2026 Codex <codex@users.noreply.github.com> - 2.5-1
- Initial openEuler riscv64 package; preserve original CTests and add installed consumers.
- Correct the canonical installed CMake config-version filename; keep exact-version checks.
