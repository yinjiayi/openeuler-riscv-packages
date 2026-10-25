# SPDX-License-Identifier: Apache-2.0
Name:           libsha2
Version:        1.1.5
Release:        1
Summary:        Bit-oriented SHA-2 family hashing library
License:        ISC
URL:            https://codeberg.org/maandree/libsha2
Source0:        https://codeberg.org/maandree/libsha2/archive/%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  binutils
BuildRequires:  glibc-devel
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  diffutils

%description
Portable bit-oriented SHA-2 family hashing library, including SHA-224/256,
SHA-384/512, SHA-512/224 and SHA-512/256, HMAC and state serialization APIs.

%package devel
Summary:        Static library, header and manual pages for libsha2
Requires:       %{name} = %{version}-%{release}

%description devel
Complete upstream development files and API manual pages.

%package tests
Summary:        Complete original libsha2 tests for installed-library replays
Requires:       %{name}-devel = %{version}-%{release}
Requires:       gcc
Requires:       glibc-devel
Requires:       binutils
Requires:       tar
Requires:       gzip
Requires:       coreutils
Requires:       diffutils

%description tests
Complete original archive for full installed shared and static test replays,
including all16 original huge-message cases rather than a filtered subset.

%prep
%autosetup -n libsha2

%build
%make_build CONFIGFILE=config-portable.mk OS=linux CC="gcc -std=c11" CFLAGS="%{optflags} -Wall" LDFLAGS="%{?build_ldflags}"

%install
make install CONFIGFILE=config-portable.mk OS=linux PREFIX=%{_prefix} MANPREFIX=%{_mandir} DESTDIR=%{buildroot}
mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}
install -d %{buildroot}%{_datadir}/libsha2/qa
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/libsha2/qa/libsha2-%{version}.tar.gz

%check
make check CONFIGFILE=config-portable.mk OS=linux CC="gcc -std=c11" CFLAGS="%{optflags} -Wall" LDFLAGS="%{?build_ldflags}" CHECK_PREFIX= CHECK_FLAGS=
run_installed_tests() (
    set -eux
    root=$1
    archive="$root/usr/share/libsha2/qa/libsha2-1.1.5.tar.gz"
    echo '7924ff2d6ac6ac3e8e8845db0c986b03cc7cad53a026cf382a0a15218d9daca1  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    tar -xzf "$archive" -C "$work" --strip-components=1
    cmp -- "$work/libsha2.h" "$root/usr/include/libsha2.h"
    test "$(grep -Ec '^[[:space:]]*test_repeated_huge\(' "$work/test.c")" = 16
    gcc -std=c11 -D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -O2 -g -Wall "$work/test.c" -L"$root/usr/lib64" -Wl,-rpath,"$root/usr/lib64" -lsha2 -o "$work/test-shared"
    readelf -d "$work/test-shared" | grep 'Shared library: \[libsha2.so.1\]'
    gcc -std=c11 -D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -O2 -g -Wall "$work/test.c" "$root/usr/lib64/libsha2.a" -o "$work/test-static"
    LD_LIBRARY_PATH="$root/usr/lib64" "$work/test-shared"
    "$work/test-static"
    echo 'PASS libsha2 complete original tests including all16 huge cases against installed shared and static libraries'
)
run_installed_tests '%{buildroot}'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc README
%{_libdir}/libsha2.so.1*

%files devel
%license LICENSE
%{_includedir}/libsha2.h
%{_libdir}/libsha2.so
%{_libdir}/libsha2.a
%{_mandir}/man0/libsha2.h.0*
%{_mandir}/man3/libsha2_*.3*
%{_mandir}/man7/libsha2.7*

%files tests
%license LICENSE
%{_datadir}/libsha2/

%changelog
* Mon Oct 19 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.1.5-1
- Use upstream portable C configuration and preserve the complete default suite.
