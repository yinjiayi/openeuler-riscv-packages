# SPDX-License-Identifier: Apache-2.0
Name:           libabort
Version:        1.0
Release:        1
Summary:        String functions that abort on truncated output
License:        ISC
URL:            https://codeberg.org/maandree/libabort
Source0:        https://codeberg.org/maandree/libabort/archive/%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  binutils
BuildRequires:  glibc-devel
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  diffutils

%description
Bounded string operations that abort if their output cannot fit or a string
has no NUL terminator within the supplied bound.

%package devel
Summary:        Public header, manuals and static library for libabort
Requires:       %{name} = %{version}-%{release}

%description devel
The original public header, manuals, shared linker name and static library.

%package tests
Summary:        All original libabort drivers and source archive
Requires:       %{name}-devel = %{version}-%{release}
Requires:       gcc
Requires:       glibc-devel
Requires:       binutils
Requires:       tar
Requires:       gzip
Requires:       coreutils
Requires:       diffutils

%description tests
Complete unchanged original test drivers and archive for installed shared
and static library replays. The upstream vsaprintf driver is a no-op because
upstream covers that function via saprintf.

%prep
%autosetup -n libabort

%build
%make_build CC="gcc -std=c99" CFLAGS="%{optflags} -Wall" LDFLAGS="%{?build_ldflags}"

%install
make install PREFIX=%{_prefix} DESTDIR=%{buildroot}
mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}
install -d %{buildroot}%{_datadir}/libabort/qa
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/libabort/qa/libabort-%{version}.tar.gz

%check
make check CC="gcc -std=c99" CFLAGS="%{optflags} -Wall" LDFLAGS="%{?build_ldflags}"
run_installed_tests() (
    set -eux
    root=$1
    archive="$root/usr/share/libabort/qa/libabort-1.0.tar.gz"
    echo '7ca1c0762ed7cf439f5d6d548bcc62b0dd0830edab26810b9ea0bbd2c7a4656f  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    tar -xzf "$archive" -C "$work" --strip-components=1
    cmp -- "$work/libabort.h" "$root/usr/include/libabort.h"
    cd "$work"
    for api in stracpy stpacpy stracat stralen stpacat saprintf vsaprintf; do
        gcc -std=c99 -D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -D_GNU_SOURCE -DTEST -fno-inline -O2 -g -Wall "libabort_$api.c" -L"$root/usr/lib64" -Wl,-rpath,"$root/usr/lib64" -labort -o "$api-shared"
        gcc -std=c99 -D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -D_GNU_SOURCE -DTEST -fno-inline -O2 -g -Wall "libabort_$api.c" "$root/usr/lib64/libabort.a" -o "$api-static"
        LD_LIBRARY_PATH="$root/usr/lib64" "./$api-shared"
        "./$api-static"
        echo "PASS libabort original $api driver shared and static"
    done
    readelf -d stracpy-shared | grep 'Shared library: \[libabort.so.1\]'
    echo 'PASS libabort all seven original drivers against installed shared and static libraries'
)
run_installed_tests '%{buildroot}'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc README
%{_libdir}/libabort.so.1*

%files devel
%license LICENSE
%{_includedir}/libabort.h
%{_libdir}/libabort.so
%{_libdir}/libabort.a
%{_mandir}/man3/libabort_*.3*
%{_mandir}/man3/*.3libabort*
%{_mandir}/man7/libabort.7*

%files tests
%license LICENSE
%{_datadir}/libabort/

%changelog
* Mon Oct 19 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.0-1
- Preserve all seven original defaults and complete installed-library replays.
