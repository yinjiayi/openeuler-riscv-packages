# SPDX-License-Identifier: Apache-2.0
Name:           libkeccak
Version:        1.4.3
Release:        1
Summary:        Bit-oriented Keccak-family hashing library
License:        ISC
URL:            https://codeberg.org/maandree/libkeccak
Source0:        https://codeberg.org/maandree/libkeccak/archive/%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  binutils
BuildRequires:  glibc-devel
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  diffutils

%description
Portable bit-oriented Keccak-family library, including SHA-3, SHAKE, cSHAKE,
state serialization and HMAC interfaces.

%package devel
Summary:        Public headers, manuals and static library for libkeccak
Requires:       %{name} = %{version}-%{release}

%description devel
The complete upstream public headers, manual pages, shared linker name and
static library.

%package tests
Summary:        Complete original libkeccak driver and fixture
Requires:       %{name}-devel = %{version}-%{release}
Requires:       gcc
Requires:       glibc-devel
Requires:       binutils
Requires:       tar
Requires:       gzip
Requires:       coreutils
Requires:       diffutils

%description tests
Full original source archive and unchanged eight-group default driver for
complete installed shared and static library replays.

%prep
%autosetup -n libkeccak

%build
%make_build CC="gcc -std=c99" CFLAGS="%{optflags} -Wall" LDFLAGS="%{?build_ldflags}"

%install
make install PREFIX=%{_prefix} DESTDIR=%{buildroot}
mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}
install -d %{buildroot}%{_datadir}/libkeccak/qa
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/libkeccak/qa/libkeccak-%{version}.tar.gz

%check
make check CC="gcc -std=c99" CFLAGS="%{optflags} -Wall" LDFLAGS="%{?build_ldflags}" CHECK_PREFIX=
run_installed_tests() (
    set -eux
    root=$1
    archive="$root/usr/share/libkeccak/qa/libkeccak-1.4.3.tar.gz"
    echo 'e395732342c9a6cbc22d709434a9d7b40f7b958952e9061ec09ec6d80d7ce83f  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    tar -xzf "$archive" -C "$work" --strip-components=1
    cmp -- "$work/libkeccak.h" "$root/usr/include/libkeccak.h"
    for header in keccak sha3 rawshake shake cshake extra hmac legacy util; do
        cmp -- "$work/libkeccak/$header.h" "$root/usr/include/libkeccak/$header.h"
    done
    cd "$work"
    echo 'e21d814d21ca269246849cc105faec1a71ac7d1cdb1a86023254f49d51b47231  .testfile' | sha256sum -c -
    gcc -std=c99 -D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -O2 -g -Wall test.c -L"$root/usr/lib64" -Wl,-rpath,"$root/usr/lib64" -lkeccak -o test-shared
    readelf -d test-shared | grep 'Shared library: \[libkeccak.so.1\]'
    gcc -std=c99 -D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -O2 -g -Wall test.c "$root/usr/lib64/libkeccak.a" -o test-static
    LD_LIBRARY_PATH="$root/usr/lib64" ./test-shared > shared.log
    cat shared.log
    if grep -F 'Fail' shared.log; then exit 1; fi
    ./test-static > static.log
    cat static.log
    if grep -F 'Fail' static.log; then exit 1; fi
    echo 'PASS libkeccak complete original eight-group driver against installed shared and static libraries'
)
run_installed_tests '%{buildroot}'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc README
%{_libdir}/libkeccak.so.1*

%files devel
%license LICENSE
%{_includedir}/libkeccak.h
%{_includedir}/libkeccak/
%{_libdir}/libkeccak.so
%{_libdir}/libkeccak.a
%{_mandir}/man3/libkeccak_*.3*
%{_mandir}/man7/libkeccak.7*

%files tests
%license LICENSE
%{_datadir}/libkeccak/

%changelog
* Mon Oct 19 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.4.3-1
- Preserve the complete original defaults and installed-library replays.
