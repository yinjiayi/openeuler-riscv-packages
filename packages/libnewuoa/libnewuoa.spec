# SPDX-License-Identifier: Apache-2.0
Name:           libnewuoa
Version:        0.1.2
Release:        1%{?dist}
Summary:        C++ NEWUOA derivative-free minimizer with a C interface
License:        MIT
URL:            https://github.com/elsid/newuoa-cpp
Source0:        libnewuoa-0.1.2.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  pkgconf
Requires:       gcc
Requires:       gcc-c++
Requires:       cmake
Requires:       make
Requires:       pkgconf

%description
NEWUOA derivative-free numerical minimization implemented in standard C++11,
with a C interface and mutable/const closures. Retain the original default
static library, public header and CMake/pkg-config consumer metadata.

%prep
%setup -q -n newuoa-cpp-8a7d5164a2a9db3756d3e8d5d9b5e67ab2a775f8

%build
%cmake_conf -DBUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_LIBDIR=lib64 -DCMAKE_INSTALL_INCLUDEDIR=include
%cmake_build

%install
%cmake_install
install -d %{buildroot}%{_datadir}/libnewuoa/tests/src \
  %{buildroot}%{_datadir}/libnewuoa/tests/include
install -m 0644 src/example_function.c src/example_closure.cpp %{buildroot}%{_datadir}/libnewuoa/tests/src/
install -m 0644 include/newuoa.h %{buildroot}%{_datadir}/libnewuoa/tests/include/
sha256sum src/example_function.c src/example_closure.cpp include/newuoa.h > %{buildroot}%{_datadir}/libnewuoa/tests/SHA256SUMS
cat > %{buildroot}%{_datadir}/libnewuoa/tests/run-checks.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
root=${1:-}
prefix="$root/usr"
base="$prefix/share/libnewuoa/tests"
(cd "$base"; sha256sum -c SHA256SUMS)
cmp "$base/include/newuoa.h" "$prefix/include/newuoa.h"
test -f "$prefix/lib64/libnewuoa.a"
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
gcc -std=c99 -UNDEBUG -I"$prefix/include" -c "$base/src/example_function.c" -o "$work/example_function.o"
g++ "$work/example_function.o" "$prefix/lib64/libnewuoa.a" -lm -o "$work/example_function"
g++ -std=gnu++11 -UNDEBUG -I"$prefix/include" "$base/src/example_closure.cpp" "$prefix/lib64/libnewuoa.a" -lm -o "$work/example_closure"
for name in example_function example_closure; do
  "$work/$name" > "$work/$name.log"
  grep -F 'function_calls_count:' "$work/$name.log"
  grep -F 'result:' "$work/$name.log"
done
cat > "$work/consumer.cpp" <<'CPP'
#include <newuoa.h>
#include <cmath>
#include <cstdio>
#include <vector>
struct State { double a,b; long calls; };
static long plain_calls=0;
static double value(long n,const double* x,double a,double b) {
    if(n!=2) return NAN;
    return (x[0]-a)*(x[0]-a)+2.0*(x[1]-b)*(x[1]-b);
}
static double plain(long n,const double* x) { ++plain_calls;return value(n,x,1.25,-2.5); }
static double mutable_callback(void* p,long n,const double* x) {
    State* s=static_cast<State*>(p);++s->calls;return value(n,x,s->a,s->b);
}
static long const_calls=0;
static double const_callback(const void* p,long n,const double* x) {
    const State* s=static_cast<const State*>(p);++const_calls;return value(n,x,s->a,s->b);
}
static bool accepted(double f,const double* x,double a,double b,long calls) {
    return std::isfinite(f) && std::isfinite(x[0]) && std::isfinite(x[1]) &&
        std::abs(f)<1e-6 && std::abs(x[0]-a)<1e-4 && std::abs(x[1]-b)<1e-4 && calls>0 && calls<=500;
}
int main() {
    const long n=2,npt=6;
    std::vector<double> w(NEWUOA_WORKING_SPACE_SIZE(n,npt));
    double x1[2]={4.0,5.0},x2[2]={0.0,0.0},x3[2]={-5.0,-5.0};
    double f1=newuoa(plain,n,npt,x1,1.0,1e-8,500,w.data());
    if(!accepted(f1,x1,1.25,-2.5,plain_calls)) return 1;
    State mutable_state={-2.0,3.0,0};
    NewuoaClosure closure={&mutable_state,mutable_callback};
    double f2=newuoa_closure(&closure,n,npt,x2,1.0,1e-8,500,w.data());
    if(!accepted(f2,x2,-2.0,3.0,mutable_state.calls)) return 2;
    const State const_state={0.5,1.5,0};
    const NewuoaClosureConst const_closure={&const_state,const_callback};
    double f3=newuoa_closure_const(&const_closure,n,npt,x3,1.0,1e-8,500,w.data());
    if(!accepted(f3,x3,0.5,1.5,const_calls)) return 3;
    std::puts("PASS downstream api-minimizers=3 finite-minimum-coordinate-and-call-bound-checks=3 skips=0");
}
CPP
PKG_CONFIG_PATH="$prefix/lib64/pkgconfig" PKG_CONFIG_SYSROOT_DIR="$root" pkg-config --exists --exact-version=0.1.2 newuoa
g++ -std=c++11 -UNDEBUG "$work/consumer.cpp" \
  $(PKG_CONFIG_PATH="$prefix/lib64/pkgconfig" PKG_CONFIG_SYSROOT_DIR="$root" pkg-config --cflags --libs newuoa) -o "$work/direct"
"$work/direct"
cat > "$work/CMakeLists.txt" <<'CMAKE'
cmake_minimum_required(VERSION 3.16)
project(newuoa_consumer LANGUAGES CXX)
find_package(newuoa 0.1.2 EXACT CONFIG REQUIRED)
add_executable(consumer consumer.cpp)
target_link_libraries(consumer PRIVATE newuoa::newuoa)
target_compile_features(consumer PRIVATE cxx_std_11)
target_compile_options(consumer PRIVATE -UNDEBUG)
CMAKE
cmake -S "$work" -B "$work/build" -DCMAKE_PREFIX_PATH="$prefix" \
  -DCMAKE_FIND_ROOT_PATH="$root" -Dnewuoa_DIR="$prefix/lib64/cmake/newuoa" \
  -DCMAKE_FIND_ROOT_PATH_MODE_LIBRARY=ONLY -DCMAKE_FIND_ROOT_PATH_MODE_INCLUDE=ONLY
cmake --build "$work/build" --verbose
"$work/build/consumer"
echo 'PASS downstream original-examples=2 installed-header-hash=1 metadata-consumers=2 skips=0'
SH
chmod 0755 %{buildroot}%{_datadir}/libnewuoa/tests/run-checks.sh

%check
# No registered upstream test suite. Retain both unchanged examples and run
# explicitly downstream semantic and consumer checks on staged installed bytes.
bash %{buildroot}%{_datadir}/libnewuoa/tests/run-checks.sh %{buildroot}

%files
%license LICENSE src/newuoa.cpp
%{_includedir}/newuoa.h
%{_libdir}/libnewuoa.a
%{_libdir}/pkgconfig/newuoa.pc
%{_libdir}/cmake/newuoa/
%{_datadir}/libnewuoa/

%changelog
* Sat Oct 17 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.2-1
- Pin official stable source, retain default static library and original examples.
- Keep complete MIT notices; add labelled downstream three-API and consumer checks.
