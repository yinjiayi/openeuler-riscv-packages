# SPDX-License-Identifier: Apache-2.0
Name:           libnsgif
Version:        1.0.0
Release:        1
Summary:        NetSurf GIF image and animation decoding library
License:        MIT AND ISC
URL:            https://netsurf-browser.org/projects/libnsgif
Source0:        https://download.netsurf-browser.org/libs/releases/libnsgif-%{version}-src.tar.gz
Source1:        https://raw.githubusercontent.com/spdx/license-list-data/d46e94e2c78ceede1cfc63cfa0396472d2798d4c/text/ISC.txt
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  binutils
BuildRequires:  glibc-devel
BuildRequires:  pkgconfig
BuildRequires:  netsurf-buildsystem >= 1.10
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  which

%description
C library for decoding GIF images and animations.

%package devel
Summary:        Headers, static library and pkg-config metadata for libnsgif
Requires:       %{name} = %{version}-%{release}

%description devel
Development files including the original default static library.

%package tests
Summary:        Complete original libnsgif corpus and installed-library replays
Requires:       %{name}-devel = %{version}-%{release}
Requires:       gcc
Requires:       glibc-devel
Requires:       binutils
Requires:       tar
Requires:       gzip
Requires:       coreutils
Requires:       diffutils

%description tests
Unchanged source archive, GIF/PPM corpus and original test driver for replaying
the full upstream script against installed shared and static libraries.

%prep
%autosetup -n libnsgif-%{version}
cp -p %{SOURCE1} ISC.txt

%build
export CFLAGS="%{optflags}"
export LDFLAGS="%{?build_ldflags}"
%make_build PREFIX=%{_prefix} LIBDIR=lib64 NSSHARED=%{_datadir}/netsurf-buildsystem BUILDDIR=build-static
%make_build PREFIX=%{_prefix} LIBDIR=lib64 NSSHARED=%{_datadir}/netsurf-buildsystem BUILDDIR=build-shared COMPONENT_TYPE=lib-shared

%install
make install PREFIX=%{_prefix} LIBDIR=lib64 NSSHARED=%{_datadir}/netsurf-buildsystem BUILDDIR=build-static DESTDIR=%{buildroot}
make install PREFIX=%{_prefix} LIBDIR=lib64 NSSHARED=%{_datadir}/netsurf-buildsystem BUILDDIR=build-shared COMPONENT_TYPE=lib-shared DESTDIR=%{buildroot}
install -d %{buildroot}%{_datadir}/libnsgif/qa
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/libnsgif/qa/libnsgif-%{version}-src.tar.gz

%check
export CFLAGS="%{optflags}"
export LDFLAGS="%{?build_ldflags}"
make test PREFIX=%{_prefix} LIBDIR=lib64 NSSHARED=%{_datadir}/netsurf-buildsystem BUILDDIR=build-static
LD_LIBRARY_PATH="$PWD/build-shared" make test PREFIX=%{_prefix} LIBDIR=lib64 NSSHARED=%{_datadir}/netsurf-buildsystem BUILDDIR=build-shared COMPONENT_TYPE=lib-shared
run_installed_tests() (
    set -eux
    root=$1
    archive="$root/usr/share/libnsgif/qa/libnsgif-1.0.0-src.tar.gz"
    echo '6014c842f61454d2f5a0f8243d7a8d7bde9b7da3ccfdca2d346c7c0b2c4c061b  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    tar -xzf "$archive" -C "$work" --strip-components=1
    cmp -- "$work/include/nsgif.h" "$root/usr/include/nsgif.h"
    mkdir "$work/shared" "$work/static"
    gcc -O2 -g -DNSGIF_NAME=nsgif -DNSGIF_VERSION=1.0.0 -I"$root/usr/include" "$work/test/nsgif.c" -L"$root/usr/lib64" -Wl,-rpath,"$root/usr/lib64" -lnsgif -lm -o "$work/shared/test_nsgif"
    readelf -d "$work/shared/test_nsgif" | grep 'Shared library: \[libnsgif.so.1\]'
    gcc -O2 -g -DNSGIF_NAME=nsgif -DNSGIF_VERSION=1.0.0 -I"$root/usr/include" "$work/test/nsgif.c" "$root/usr/lib64/libnsgif.a" -lm -o "$work/static/test_nsgif"
    cd "$work"
    LD_LIBRARY_PATH="$root/usr/lib64" sh test/runtest.sh "$work/shared" > shared-summary.log
    cat shared-summary.log "$work/shared/test.log"
    grep -E '^Tests:[1-9][0-9]* Pass:[0-9]+ Fail:[0-9]+ Error:0$' shared-summary.log
    sh test/runtest.sh "$work/static" > static-summary.log
    cat static-summary.log "$work/static/test.log"
    grep -E '^Tests:[1-9][0-9]* Pass:[0-9]+ Fail:[0-9]+ Error:0$' static-summary.log
    echo 'PASS libnsgif full unchanged corpus script against installed shared and static libraries'
)
run_installed_tests '%{buildroot}'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING ISC.txt test/cli.c test/cli.h
%doc README.md
%{_libdir}/libnsgif.so.1*

%files devel
%license COPYING ISC.txt test/cli.c test/cli.h
%{_includedir}/nsgif.h
%{_libdir}/libnsgif.so
%{_libdir}/libnsgif.a
%{_libdir}/pkgconfig/libnsgif.pc

%files tests
%license COPYING ISC.txt test/cli.c test/cli.h
%{_datadir}/libnsgif/

%changelog
* Mon Oct 19 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.0.0-1
- Preserve full upstream defaults and corpus; add shared and installed replays.
