# SPDX-License-Identifier: Apache-2.0
Name:           libblake
Version:        3.0.2.1
Release:        1
Summary:        Portable BLAKE, BLAKE2 and BLAKE2X hashing library
License:        ISC
URL:            https://codeberg.org/maandree/libblake
Source0:        https://codeberg.org/maandree/libblake/archive/%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  binutils
BuildRequires:  glibc-devel
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  diffutils

%description
Portable C implementations of the BLAKE, BLAKE2 and BLAKE2X hashing families
with all eight upstream default algorithm selections retained.

%package devel
Summary:        Header and static library for libblake
Requires:       %{name} = %{version}-%{release}

%description devel
The complete upstream public header, shared linker name and static library.

%package tests
Summary:        Complete original libblake tests and known-answer corpus
Requires:       %{name}-devel = %{version}-%{release}
Requires:       gcc
Requires:       glibc-devel
Requires:       binutils
Requires:       tar
Requires:       gzip
Requires:       coreutils
Requires:       diffutils

%description tests
Full original test driver and all four known-answer files for installed
shared and static library replays, with all eight default algorithms enabled.

%prep
%autosetup -n libblake

%build
%make_build OS=linux CC="gcc -std=c11" CFLAGS="%{optflags} -Wall" LDFLAGS="%{?build_ldflags}"

%install
make install OS=linux PREFIX=%{_prefix} DESTDIR=%{buildroot}
mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}
install -d %{buildroot}%{_datadir}/libblake/qa
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/libblake/qa/libblake-%{version}.tar.gz

%check
make check OS=linux CC="gcc -std=c11" CFLAGS="%{optflags} -Wall" LDFLAGS="%{?build_ldflags}" CHECK_PREFIX=
run_installed_tests() (
    set -eux
    root=$1
    archive="$root/usr/share/libblake/qa/libblake-3.0.2.1.tar.gz"
    echo '6855dc9fb107d13764c9619deab482ec0f20064c140989bb6b6a936ac0cc3c4d  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    tar -xzf "$archive" -C "$work" --strip-components=1
    cmp -- "$work/libblake.h" "$root/usr/include/libblake.h"
    for kat in blake2s blake2b blake2xs blake2xb; do test -s "$work/kat/$kat"; done
    gcc -std=c11 -D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -D_GNU_SOURCE -DSUPPORT_BLAKE224 -DSUPPORT_BLAKE256 -DSUPPORT_BLAKE384 -DSUPPORT_BLAKE512 -DSUPPORT_BLAKE2S -DSUPPORT_BLAKE2B -DSUPPORT_BLAKE2XS -DSUPPORT_BLAKE2XB -O2 -g -Wall "$work/test.c" -L"$root/usr/lib64" -Wl,-rpath,"$root/usr/lib64" -lblake -o "$work/test-shared"
    readelf -d "$work/test-shared" | grep 'Shared library: \[libblake.so.3\]'
    gcc -std=c11 -D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -D_GNU_SOURCE -DSUPPORT_BLAKE224 -DSUPPORT_BLAKE256 -DSUPPORT_BLAKE384 -DSUPPORT_BLAKE512 -DSUPPORT_BLAKE2S -DSUPPORT_BLAKE2B -DSUPPORT_BLAKE2XS -DSUPPORT_BLAKE2XB -O2 -g -Wall "$work/test.c" "$root/usr/lib64/libblake.a" -o "$work/test-static"
    cd "$work"
    LD_LIBRARY_PATH="$root/usr/lib64" ./test-shared
    ./test-static
    echo 'PASS libblake complete original tests, all eight algorithms and four KAT files against installed shared and static libraries'
)
run_installed_tests '%{buildroot}'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc README
%{_libdir}/libblake.so.3*

%files devel
%license LICENSE
%{_includedir}/libblake.h
%{_libdir}/libblake.so
%{_libdir}/libblake.a

%files tests
%license LICENSE
%{_datadir}/libblake/

%changelog
* Mon Oct 19 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 3.0.2.1-1
- Preserve all upstream default algorithms and full original known-answer tests.
