# SPDX-License-Identifier: Apache-2.0
Name:           libcstl
Version:        2.3.0
Release:        1%{?dist}
Summary:        Generic C containers and algorithms with an STL-like interface
License:        LGPL-2.1-or-later
URL:            https://github.com/activesys/libcstl
Source0:        https://codeload.github.com/activesys/libcstl/tar.gz/f0fd5ccb817192614588915ab0b5dbebbc6ed58b#/libcstl-2.3.0.tar.gz
Patch0:         0001-preserve-original-suite-with-current-build-tools.patch
Patch1:         0002-type-original-test-pointer-sentinels.patch
Patch2:         0003-pass-original-basic-string-test-object-and-byte-view.patch
Patch3:         0004-correct-original-representation-test-arguments.patch
BuildRequires:  gcc glibc-devel make autoconf automake libtool libcmocka-devel
BuildRequires:  coreutils findutils grep sed patch binutils

%description
Generic C containers and algorithms with an STL-like interface. Default
container implementations and memory-management configuration are retained.

%package devel
Summary:        Headers, static library and RPM-bound libcstl consumer checks
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc glibc-devel binutils coreutils grep

%description devel
Upstream headers, static library, shared link interface, and a separately
labelled downstream consumer exercising installed containers.

%prep
%setup -q -n libcstl-f0fd5ccb817192614588915ab0b5dbebbc6ed58b
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1
%patch -P 3 -p1
autoreconf --force --install --verbose
cat > verify-containers.c <<'C'
#include <stdio.h>
#include <stdlib.h>
#include <cstl/cvector.h>
#include <cstl/clist.h>
#define CHECK(x) do { if (!(x)) { fputs("FAIL " #x "\n", stderr); exit(1); } ++checks; } while (0)
int main(void) {
    int checks = 0;
    vector_t *v = create_vector(int);
    CHECK(v != NULL);
    vector_init(v);
    CHECK(vector_empty(v));
    vector_push_back(v, 9);
    vector_push_back(v, 2);
    CHECK(vector_size(v) == 2);
    CHECK(*(int *)vector_at(v, 0) == 9);
    CHECK(*(int *)vector_at(v, 1) == 2);
    vector_pop_back(v);
    CHECK(vector_size(v) == 1);
    vector_destroy(v);
    list_t *l = create_list(int);
    CHECK(l != NULL);
    list_init(l);
    CHECK(list_empty(l));
    list_push_back(l, 7);
    list_push_front(l, 3);
    CHECK(list_size(l) == 2);
    CHECK(*(int *)list_front(l) == 3);
    CHECK(*(int *)list_back(l) == 7);
    list_destroy(l);
    CHECK(checks == 11);
    puts("PASS downstream-containers checks=12 skips=0");
    return 0;
}
C

%build
%configure CFLAGS="%{optflags} -UNDEBUG" CPPFLAGS="-I$PWD/compat"
%make_build

%install
%make_install
find %{buildroot}%{_libdir} -name '*.la' -delete
install -d %{buildroot}%{_datadir}/libcstl/tests
install -m 0644 verify-containers.c %{buildroot}%{_datadir}/libcstl/tests/
sha256sum verify-containers.c > %{buildroot}%{_datadir}/libcstl/tests/SHA256SUMS

%check
# Original registered Automake suite, with every original unit-test case.
make -j1 check VERBOSE=1
test -s test/ut/libcstl_ut.log
cat test/ut/libcstl_ut.log
test -s test/ut/libcstl_ut.trs
grep -Fx ':test-result: PASS' test/ut/libcstl_ut.trs
if grep -Eq '^:test-result: (SKIP|XFAIL|FAIL|ERROR)' test/ut/libcstl_ut.trs; then exit 1; fi
# Separately downstream checks bind staged public headers and both libraries.
gcc %{optflags} -UNDEBUG -I%{buildroot}%{_includedir} verify-containers.c \
    -L%{buildroot}%{_libdir} -lcstl -o staged-shared
LD_LIBRARY_PATH=%{buildroot}%{_libdir} ./staged-shared
gcc %{optflags} -UNDEBUG -I%{buildroot}%{_includedir} verify-containers.c \
    %{buildroot}%{_libdir}/libcstl.a -o staged-static
./staged-static

%files
%license COPYING.LESSER AUTHORS
%doc README ChangeLog VERSION
%{_libdir}/libcstl.so.2*

%files devel
%{_includedir}/cstl/
%{_libdir}/libcstl.so
%{_libdir}/libcstl.a
%{_datadir}/libcstl/

%changelog
* Thu Oct 15 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 2.3.0-1
- Pin stable source and preserve the complete original suite and defaults.
