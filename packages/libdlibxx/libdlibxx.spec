# SPDX-License-Identifier: Apache-2.0
Name:           libdlibxx
Version:        1.1.0
Release:        1%{?dist}
Summary:        C++11 dynamic library loading and symbol lookup wrapper
License:        BSD-2-Clause
URL:            https://github.com/m-renaud/libdlibxx
Source0:        libdlibxx-1.1.0.tar.gz
Patch0:         0001-use-gnu-install-dirs.patch
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  cmake
BuildRequires:  boost-devel
BuildRequires:  glibc-devel
Requires:       gcc-c++
Requires:       boost-devel
Requires:       bash
Requires:       coreutils
Requires:       grep

%description
Libdlibxx wraps POSIX dynamic library handles, function symbol lookup and plugin
factories in a C++11 interface using Boost.Optional. The original examples and
additional downstream functional acceptance are included for installed replay.

%prep
%setup -q -n libdlibxx-bbf532ad6b1d9c9cd350d9b83c73a8aff156a49e
%patch0 -p1
mkdir -p downstream
cat > downstream/consumer.cxx <<'CXX'
#include <cstdlib>
#include <iostream>
#include <string>
#include <dlibxx.hxx>
#include "plugin.hxx"
static void require(bool value, const char *message) {
  if (!value) { std::cerr << message << '\n'; std::exit(1); }
}
int main(int argc, char **argv) {
  require(argc == 2, "plugin directory required");
  const std::string dir = argv[1];
  dlibxx::handle h;
  require(!h.loaded() && !static_cast<bool>(h), "initial handle");
  require(!h.lookup<int(int,int)>("bin_op"), "closed lookup must fail");
  require(h.error() == "Handle not open.", "closed lookup error");
  h.load(dir + "/no-such-library.so");
  require(!h.loaded() && !h.error().empty(), "invalid library must fail");
  h.resolve_policy(dlibxx::resolve::now);
  h.set_options(dlibxx::options::local);
  h.load(dir + "/liba.so");
  require(h.loaded() && static_cast<bool>(h), "load a");
  require(h.get_lib_name() == dir + "/liba.so", "library name");
  { auto p = h.create<plugin>("create_plugin");
    require(p && p->name() == "plugin_a", "factory a"); }
  require(!h.lookup<int(int,int)>("bin_op"), "a has C++ mangled bin_op");
  require(!h.create<plugin>("missing_factory"), "missing factory must fail");
  h.close(); require(!h.loaded(), "close a");
  h.resolve_policy(dlibxx::resolve::lazy);
  h.load(dir + "/libb.so"); require(h.loaded(), "load b");
  { const std::string factory = "create_plugin";
    auto p = h.create<plugin>(factory);
    require(p && p->name() == "plugin_b", "string factory b"); }
  h.close();
  { dlibxx::handle c(dir + "/libc.so");
    require(c.loaded(), "constructor load c");
    const std::string symbol = "bin_op";
    auto sum = c.lookup<int(int,int)>(symbol);
    require(static_cast<bool>(sum), "C symbol lookup");
    require(sum.get()(19,23) == 42 && sum.get()(-7,4) == -3, "sum values");
    require(!c.create<plugin>("create_plugin"), "c has no factory");
    require(!c.lookup<int()>("missing_symbol"), "missing symbol must fail"); }
  std::cout << "libdlibxx downstream API acceptance: PASS\n";
}
CXX
cat > downstream/run-tests.sh <<'SH'
#!/bin/bash
set -euo pipefail
data=$(cd -- "$1" && pwd)
inc=$2
lib=$3
original=${4:-}
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
cd -- "$data"
sha256sum --strict -c SHA256SUMS
cd -- "$work"
export LD_LIBRARY_PATH="$lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
cxx=${CXX:-g++}
for name in a b c; do
  "$cxx" -std=c++11 -O2 -fPIC -shared -I"$data/examples" \
    "$data/examples/plugin-$name.cxx" -o "lib$name.so"
done
"$cxx" -std=c++11 -O2 -I"$inc" -I"$data/examples" \
  "$data/examples/demo.cxx" -L"$lib" -ldlibxx -ldl -o demo
"$cxx" -std=c++11 -O2 -I"$inc" -I"$data/examples" \
  "$data/examples/simple-dl-demo.cxx" -L"$lib" -ldlibxx -ldl -o simple-dl-demo
"$cxx" -std=c++11 -O2 -I"$inc" -I"$data/examples" \
  "$data/consumer.cxx" -L"$lib" -ldlibxx -ldl -o consumer
run_demo() {
  local demo=$1 plugins=$2 output=$3
  printf '%s\n' "$plugins/liba.so" "$plugins/libb.so" "$plugins/libc.so" | \
    "$demo" > "$output.stdout" 2> "$output.stderr"
  test "$(grep -F -c 'plugin_a::render()' "$output.stdout")" -eq 1
  test "$(grep -F -c 'plugin_b::render()' "$output.stdout")" -eq 1
  test "$(grep -F -c 'Could not create object.' "$output.stdout")" -eq 1
  test "$(grep -x -c '3' "$output.stdout")" -eq 2
  test "$(grep -F -x -c 'That symbol cannot be found.' "$output.stderr")" -eq 2
}
if test -n "$original"; then
  run_demo "$original/demo" "$original" default-build
  echo 'libdlibxx original default-built demo and three plugins: PASS'
fi
run_demo "$work/demo" "$work" recompiled
# The extra simple example has no null-factory error handling: supply only a/b.
printf '%s\n' "$work/liba.so" "$work/libb.so" | ./simple-dl-demo > simple.stdout
test "$(grep -F -c 'plugin_a::render()' simple.stdout)" -eq 1
test "$(grep -F -c 'plugin_b::render()' simple.stdout)" -eq 1
./consumer "$work"
echo 'libdlibxx original example source replay: PASS'
SH
chmod 0755 downstream/run-tests.sh
mkdir -p downstream/examples
cp examples/{plugin.hxx,plugin-a.cxx,plugin-b.cxx,plugin-c.cxx,demo.cxx,simple-dl-demo.cxx} downstream/examples/
(cd downstream && sha256sum examples/* > SHA256SUMS)

%build
cmake -S . -B build -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_INSTALL_LIBDIR=lib64 -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_CXX_FLAGS="%{optflags}"
cmake --build build --parallel %{?_smp_build_ncpus}

%install
DESTDIR=%{buildroot} cmake --install build
install -d %{buildroot}%{_datadir}/%{name}/examples
install -m 0644 downstream/{consumer.cxx,SHA256SUMS} %{buildroot}%{_datadir}/%{name}/
install -m 0755 downstream/run-tests.sh %{buildroot}%{_datadir}/%{name}/run-tests.sh
install -m 0644 downstream/examples/* %{buildroot}%{_datadir}/%{name}/examples/

%check
./downstream/run-tests.sh "$PWD/downstream" "$PWD/include" "$PWD/build" "$PWD/build/examples"
./downstream/run-tests.sh "%{buildroot}%{_datadir}/%{name}" \
  "%{buildroot}%{_includedir}" "%{buildroot}%{_libdir}"

%files
%license LICENSE
%doc README.md INSTALL.md
%{_libdir}/libdlibxx.so*
%{_includedir}/dlibxx.hxx
%{_datadir}/%{name}

%changelog
* Sat Oct 17 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.1.0-1
- Pin the official stable release, preserve shared library/default examples, and
  add staged and installed plugin/API checks without claiming native validation.
