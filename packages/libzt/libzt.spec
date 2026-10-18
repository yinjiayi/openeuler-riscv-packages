# SPDX-License-Identifier: Apache-2.0
Name:           libzt
Version:        0.3.1
Release:        1%{?dist}
Summary:        Compact C unit testing library
License:        LGPL-3.0-only
URL:            https://github.com/zyga/libzt
Source0:        https://github.com/zyga/libzt/releases/download/v%{version}/libzt_%{version}.tar.gz
Source1:        GPL-3.0.txt
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  grep
BuildRequires:  sed

%description
Libzt is a small C testing library providing claims, test suites, visitors,
diagnostics and a standalone self-test. The complete default build is retained.

%package devel
Summary:        Headers, static library and downstream libzt consumer fixture
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc glibc-devel binutils coreutils grep

%description devel
Public header, shared linking interface, static library, API manuals and an
explicitly downstream API fixture for building against installed Libzt.

%prep
%setup -q -n libzt_%{version}
cp -p %{SOURCE1} GPL-3.0.txt
# Downstream consumer; separate from the untouched original self-test suite.
cat > consumer.c <<'C'
/* SPDX-License-Identifier: Apache-2.0 */
#include <zt.h>
#include <stddef.h>
static void consumer_test(zt_t t) {
    int value = 42;
    zt_check(t, ZT_TRUE(2 + 2 == 4));
    zt_check(t, ZT_FALSE(2 + 2 == 5));
    zt_check(t, ZT_CMP_INT(value, ==, 42));
    zt_check(t, ZT_CMP_BOOL(false, ==, false));
    zt_check(t, ZT_NULL(NULL));
    zt_check(t, ZT_NOT_NULL(&value));
#ifdef NEGATIVE_CONTROL
    zt_check(t, ZT_TRUE(false));
#endif
}
static void consumer_suite(zt_visitor v) {
    ZT_VISIT_TEST_CASE(v, consumer_test);
}
int main(int argc, char **argv, char **envp) {
    return zt_main(argc, argv, envp, consumer_suite);
}
C

%build
%set_build_flags
# The bundled ZMK configure is not Autoconf: pass only its supported options.
# No cross compiler or assertion-disabling flag: original check must execute.
./configure --prefix=%{_prefix} --libdir=%{_libdir} \
    --includedir=%{_includedir} --bindir=%{_bindir} --mandir=%{_mandir} \
    CC=gcc CFLAGS="%{optflags} -UNDEBUG" LDFLAGS="$LDFLAGS"
%make_build

%install
%make_install
install -d %{buildroot}%{_datadir}/libzt/tests
install -m 0644 consumer.c %{buildroot}%{_datadir}/libzt/tests/
sha256sum consumer.c > %{buildroot}%{_datadir}/libzt/tests/SHA256SUMS

%check
# Run the complete original default suite, and reject a cross-build skip.
make -j1 check > upstream-check.log 2>&1
cat upstream-check.log
grep -Fx 'libzt self-test successful' upstream-check.log
# Separately check consumers of both staged library interfaces.
gcc %{optflags} -UNDEBUG -I%{buildroot}%{_includedir} consumer.c \
    -L%{buildroot}%{_libdir} -lzt -o staged-shared
LD_LIBRARY_PATH=%{buildroot}%{_libdir} ./staged-shared -v
gcc %{optflags} -UNDEBUG -I%{buildroot}%{_includedir} consumer.c \
    %{buildroot}%{_libdir}/libzt.a -o staged-static
./staged-static -v

%files
%license LICENSE GPL-3.0.txt
%doc README.md NEWS
%{_libdir}/libzt.so.1
%{_bindir}/libzt-test
%{_mandir}/man1/libzt-test.1*

%files devel
%{_includedir}/zt.h
%{_libdir}/libzt.so
%{_libdir}/libzt.a
%{_mandir}/man3/libzt.3*
%{_mandir}/man3/zt_*.3*
%{_mandir}/man3/ZT_*.3*
%{_datadir}/libzt/

%changelog
* Fri Oct 16 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 0.3.1-1
- Pin the official signed release with bundled ZMK and complete original tests.
