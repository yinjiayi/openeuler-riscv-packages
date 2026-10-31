# SPDX-License-Identifier: MIT
%global debug_package %{nil}
%global upstream_commit 720f62bddb7226106071d4728c292cb1df519ceb

Name:           qrcodegen
Version:        1.8.0
Release:        1
Summary:        Nayuki QR Code generator C and C++ static libraries
License:        MIT
URL:            https://www.nayuki.io/page/qr-code-generator-library
Source0:        https://codeload.github.com/nayuki/QR-Code-generator/tar.gz/%{upstream_commit}#/qrcodegen-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  binutils
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  grep
BuildRequires:  diffutils

%description
Original independent C and C++ QR Code generator implementations with public
headers and static development archives. Other language ports are not packaged.

%package tests
Summary:        Original public-API demos and deterministic reference outputs
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc
Requires:       gcc-c++
Requires:       bash
Requires:       coreutils
Requires:       diffutils

%description tests
Unmodified C and C++ demos replayed against the installed static archives.
The complete C internal test suite is separately preserved in the build check;
it requires an instrumented implementation, not the installed public archive.

%prep
%setup -q -n QR-Code-generator-%{upstream_commit}

%build
make -C c all CC=gcc AR=ar CFLAGS='%{optflags} -UNDEBUG -std=c99 -O'
make -C cpp all CXX=g++ AR=ar CXXFLAGS='%{optflags} -UNDEBUG -std=c++11 -O'
./c/qrcodegen-demo > c-demo.expected
./cpp/QrCodeGeneratorDemo > cpp-demo.expected
test -s c-demo.expected
test -s cpp-demo.expected

%install
mkdir -p %{buildroot}%{_includedir}/qrcodegen %{buildroot}%{_libdir}
install -pm0644 c/qrcodegen.h cpp/qrcodegen.hpp %{buildroot}%{_includedir}/qrcodegen/
install -pm0644 c/libqrcodegen.a cpp/libqrcodegencpp.a %{buildroot}%{_libdir}/
mkdir -p %{buildroot}%{_datadir}/qrcodegen/qa
install -pm0644 c/qrcodegen-demo.c %{buildroot}%{_datadir}/qrcodegen/qa/c-demo.c
install -pm0644 cpp/QrCodeGeneratorDemo.cpp %{buildroot}%{_datadir}/qrcodegen/qa/cpp-demo.cpp
install -pm0644 c-demo.expected cpp-demo.expected %{buildroot}%{_datadir}/qrcodegen/qa/

%check
./c/qrcodegen-test > complete-c-tests.log
cat complete-c-tests.log
grep -Ex 'All [1-9][0-9]* test cases passed' complete-c-tests.log
run_installed_demos() {
    root=$1
    qa="$root/usr/share/qrcodegen/qa"
    temp=$(mktemp -d)
    gcc -O2 -g -UNDEBUG -std=c99 -I"$root/usr/include/qrcodegen" "$qa/c-demo.c" "$root/usr/lib64/libqrcodegen.a" -o "$temp/c-demo"
    g++ -O2 -g -UNDEBUG -std=c++11 -I"$root/usr/include/qrcodegen" "$qa/cpp-demo.cpp" "$root/usr/lib64/libqrcodegencpp.a" -o "$temp/cpp-demo"
    "$temp/c-demo" > "$temp/c.out"
    "$temp/cpp-demo" > "$temp/cpp.out"
    cmp "$qa/c-demo.expected" "$temp/c.out"
    cmp "$qa/cpp-demo.expected" "$temp/cpp.out"
    rm -f "$temp/c-demo" "$temp/cpp-demo" "$temp/c.out" "$temp/cpp.out"
    rmdir "$temp"
    echo 'PASS qrcodegen complete original C/C++ demos against installed static archives'
}
run_installed_demos '%{buildroot}'

%files
%license Readme.markdown
%{_includedir}/qrcodegen
%{_libdir}/libqrcodegen.a
%{_libdir}/libqrcodegencpp.a

%files tests
%license Readme.markdown
%{_datadir}/qrcodegen

%changelog
* Sun Oct 18 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.8.0-1
- Preserve complete original C tests and both C/C++ default build targets.
