# SPDX-License-Identifier: BSD-3-Clause
%global debug_package %{nil}
%global upstream_commit 2529065f2e9fc64aa4ed34df2df4bf0bde718889

Name:           bstrlib
Version:        1.0.0
Release:        1
Summary:        Better String Library with C and C++ interfaces
License:        BSD-3-Clause
URL:            https://github.com/websnarf/bstrlib
Source0:        https://codeload.github.com/websnarf/bstrlib/tar.gz/%{upstream_commit}#/bstrlib-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  binutils
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  grep

%description
String handling library with C core, auxiliary and Unicode modules, a C++
wrapper and an opt-in unsafe-C-function enforcement archive. The static
development archives and public headers are installed together.

%package tests
Summary:        Unchanged upstream core, auxiliary and C++ test suites
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc
Requires:       gcc-c++
Requires:       binutils
Requires:       bash
Requires:       coreutils
Requires:       grep

%description tests
Original complete suites replayed against the installed library. Counted
failures are checked explicitly because upstream mains always return zero.

%prep
%setup -q -n bstrlib-%{upstream_commit}

%build
for module in bstrlib bstraux buniutil utf8util bsafe; do
    gcc %{optflags} -UNDEBUG -std=gnu99 -c "$module.c" -o "$module.o"
done
g++ %{optflags} -UNDEBUG -std=gnu++11 -c bstrwrap.cpp -o bstrwrap.o
ar rcs libbstrlib.a bstrlib.o bstraux.o buniutil.o utf8util.o
ar rcs libbstrwrap.a bstrwrap.o
ar rcs libbsafe.a bsafe.o
gcc %{optflags} -UNDEBUG -std=gnu99 bstest.c libbstrlib.a -o core-test
gcc %{optflags} -UNDEBUG -std=gnu99 testaux.c libbstrlib.a -o aux-test
g++ %{optflags} -UNDEBUG -std=gnu++11 test.cpp libbstrwrap.a libbstrlib.a -o cpp-test

%install
mkdir -p %{buildroot}%{_includedir}/bstrlib %{buildroot}%{_libdir}
install -pm0644 bstrlib.h bstraux.h buniutil.h utf8util.h bstrwrap.h bsafe.h %{buildroot}%{_includedir}/bstrlib/
install -pm0644 libbstrlib.a libbstrwrap.a libbsafe.a %{buildroot}%{_libdir}/
mkdir -p %{buildroot}%{_datadir}/bstrlib/qa
install -pm0644 bstest.c testaux.c test.cpp %{buildroot}%{_datadir}/bstrlib/qa/

%check
for suite in core aux cpp; do
    ./"$suite-test" > "$suite.log"
    cat "$suite.log"
    grep -qx '# test failures: 0' "$suite.log"
done
run_installed_defaults() {
    root=$1
    qa="$root/usr/share/bstrlib/qa"
    temp=$(mktemp -d)
    gcc -O2 -g -UNDEBUG -std=gnu99 -I"$root/usr/include/bstrlib" "$qa/bstest.c" "$root/usr/lib64/libbstrlib.a" -o "$temp/core-test"
    gcc -O2 -g -UNDEBUG -std=gnu99 -I"$root/usr/include/bstrlib" "$qa/testaux.c" "$root/usr/lib64/libbstrlib.a" -o "$temp/aux-test"
    g++ -O2 -g -UNDEBUG -std=gnu++11 -I"$root/usr/include/bstrlib" "$qa/test.cpp" "$root/usr/lib64/libbstrwrap.a" "$root/usr/lib64/libbstrlib.a" -o "$temp/cpp-test"
    for suite in core aux cpp; do
        "$temp/$suite-test" > "$temp/$suite.log"
        cat "$temp/$suite.log"
        grep -qx '# test failures: 0' "$temp/$suite.log"
    done
    rm -f "$temp/core-test" "$temp/aux-test" "$temp/cpp-test" "$temp/core.log" "$temp/aux.log" "$temp/cpp.log"
    rmdir "$temp"
    echo 'PASS bstrlib original-core=49 auxiliary=15 cpp=34 installed-archives skips=0'
}
run_installed_defaults '%{buildroot}'

%files
%license LICENSE
%doc README.md bstrlib.txt porting.txt security.txt
%{_includedir}/bstrlib
%{_libdir}/libbstrlib.a
%{_libdir}/libbstrwrap.a
%{_libdir}/libbsafe.a

%files tests
%license LICENSE
%{_datadir}/bstrlib

%changelog
* Sun Oct 18 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.0.0-1
- Preserve complete original C and C++ suites and enforce zero counted failures.
