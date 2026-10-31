# SPDX-License-Identifier: Apache-2.0
Name:           libterminput
Version:        1.1.2
Release:        1
Summary:        Terminal input parsing library
License:        ISC
URL:            https://codeberg.org/maandree/libterminput
Source0:        https://codeberg.org/maandree/libterminput/archive/%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  binutils
BuildRequires:  glibc-devel
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  diffutils

%description
Parse common terminal input sequences, including key and mouse events,
bracketed paste and serialized input state, without a terminfo dependency.

%package devel
Summary:        Public header, manuals and static library for libterminput
Requires:       %{name} = %{version}-%{release}

%description devel
The original public header, manual pages, shared linker name and static library.

%package tests
Summary:        Complete original libterminput test driver and source archive
Requires:       %{name}-devel = %{version}-%{release}
Requires:       gcc
Requires:       glibc-devel
Requires:       binutils
Requires:       tar
Requires:       gzip
Requires:       coreutils
Requires:       diffutils

%description tests
Unchanged original pipe-based default driver and source archive for full
installed shared and static library replays.

%prep
%autosetup -n libterminput

%build
%make_build CC="gcc -std=c99" CFLAGS="%{optflags} -Wall" LDFLAGS="%{?build_ldflags}"

%install
make install PREFIX=%{_prefix} DESTDIR=%{buildroot}
mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}
install -d %{buildroot}%{_datadir}/libterminput/qa
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/libterminput/qa/libterminput-%{version}.tar.gz

%check
make check CC="gcc -std=c99" CFLAGS="%{optflags} -Wall" LDFLAGS="%{?build_ldflags}"
run_installed_tests() (
    set -eux
    root=$1
    archive="$root/usr/share/libterminput/qa/libterminput-1.1.2.tar.gz"
    echo '2757ca59bf4e08e63788e368eb340d9f4784b7aa3da965f35ea53be15acd0ffc  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    tar -xzf "$archive" -C "$work" --strip-components=1
    cmp -- "$work/libterminput.h" "$root/usr/include/libterminput.h"
    cd "$work"
    gcc -std=c99 -D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -O2 -g -Wall test.c -L"$root/usr/lib64" -Wl,-rpath,"$root/usr/lib64" -lterminput -o test-shared
    readelf -d test-shared | grep 'Shared library: \[libterminput.so.1\]'
    gcc -std=c99 -D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -O2 -g -Wall test.c "$root/usr/lib64/libterminput.a" -o test-static
    LD_LIBRARY_PATH="$root/usr/lib64" ./test-shared
    ./test-static
    echo 'PASS libterminput complete original pipe-based driver against installed shared and static libraries'
)
run_installed_tests '%{buildroot}'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc README
%{_libdir}/libterminput.so.1*

%files devel
%license LICENSE
%{_includedir}/libterminput.h
%{_libdir}/libterminput.so
%{_libdir}/libterminput.a
%{_mandir}/man3/libterminput_*.3*
%{_mandir}/man7/libterminput.7*

%files tests
%license LICENSE
%{_datadir}/libterminput/

%changelog
* Mon Oct 19 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.1.2-1
- Preserve the full original default tests and installed-library replays.
