# SPDX-License-Identifier: Apache-2.0
Name:           libsha1
Version:        1.1.6
Release:        1
Summary:        Bit-oriented SHA-1 and SHA-0 hashing library
License:        ISC
URL:            https://codeberg.org/maandree/libsha1
Source0:        https://codeberg.org/maandree/libsha1/archive/%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  binutils
BuildRequires:  glibc-devel
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  diffutils

%description
Portable bit-oriented SHA-1 and SHA-0 hashing library, including HMAC and
state serialization APIs. Availability does not imply suitability for new
security-sensitive applications.

%package devel
Summary:        Static library, header and manual pages for libsha1
Requires:       %{name} = %{version}-%{release}

%description devel
Complete upstream development files and API manual pages.

%package tests
Summary:        Complete original libsha1 tests for installed-library replays
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
including every original huge-message test rather than a filtered subset.

%prep
%autosetup -n libsha1

%build
%make_build CONFIGFILE=config-portable.mk OS=linux CC="gcc -std=c11" CFLAGS="%{optflags} -Wall" LDFLAGS="%{?build_ldflags}"

%install
make install CONFIGFILE=config-portable.mk OS=linux PREFIX=%{_prefix} MANPREFIX=%{_mandir} DESTDIR=%{buildroot}
mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}
install -d %{buildroot}%{_datadir}/libsha1/qa
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/libsha1/qa/libsha1-%{version}.tar.gz

%check
make check CONFIGFILE=config-portable.mk OS=linux CC="gcc -std=c11" CFLAGS="%{optflags} -Wall" LDFLAGS="%{?build_ldflags}"
run_installed_tests() (
    set -eux
    root=$1
    archive="$root/usr/share/libsha1/qa/libsha1-1.1.6.tar.gz"
    echo '55536baac47e1cc62ed33d87bbe1ffa42a96871c2d4e6c06ff81b7dc072d9318  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    tar -xzf "$archive" -C "$work" --strip-components=1
    cmp -- "$work/libsha1.h" "$root/usr/include/libsha1.h"
    test "$(grep -Ec '^[[:space:]]*test_repeated_huge\(' "$work/test.c")" = 4
    gcc -std=c11 -D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -O2 -g -Wall "$work/test.c" -L"$root/usr/lib64" -Wl,-rpath,"$root/usr/lib64" -lsha1 -o "$work/test-shared"
    readelf -d "$work/test-shared" | grep 'Shared library: \[libsha1.so.1\]'
    gcc -std=c11 -D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -O2 -g -Wall "$work/test.c" "$root/usr/lib64/libsha1.a" -o "$work/test-static"
    LD_LIBRARY_PATH="$root/usr/lib64" "$work/test-shared"
    "$work/test-static"
    echo 'PASS libsha1 complete original tests including four huge cases against installed shared and static libraries'
)
run_installed_tests '%{buildroot}'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc README
%{_libdir}/libsha1.so.1*

%files devel
%license LICENSE
%{_includedir}/libsha1.h
%{_libdir}/libsha1.so
%{_libdir}/libsha1.a
%{_mandir}/man0/libsha1.h.0*
%{_mandir}/man3/libsha1_*.3*
%{_mandir}/man7/libsha1.7*

%files tests
%license LICENSE
%{_datadir}/libsha1/

%changelog
* Mon Oct 19 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.1.6-1
- Use upstream portable C configuration and preserve the complete default suite.
