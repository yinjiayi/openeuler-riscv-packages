# SPDX-License-Identifier: Apache-2.0
Name:           libnsutils
Version:        0.1.1
Release:        1
Summary:        Utility library for NetSurf applications
License:        MIT
URL:            https://source.netsurf-browser.org/libnsutils
Source0:        https://download.netsurf-browser.org/libs/releases/libnsutils-%{version}-src.tar.gz
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
NetSurf utilities for base64 conversion, time and POSIX descriptor operations.

%package devel
Summary:        Headers, static library and pkg-config metadata for libnsutils
Requires:       %{name} = %{version}-%{release}

%description devel
Development files including the original default static library.

%package tests
Summary:        Unchanged original libnsutils source and installed-library checks
Requires:       %{name}-devel = %{version}-%{release}
Requires:       gcc
Requires:       glibc-devel
Requires:       binutils
Requires:       tar
Requires:       gzip
Requires:       coreutils
Requires:       diffutils

%description tests
Complete original release archive for replaying the unchanged base64 driver
and all 32 original assertions against installed shared and static libraries.

%prep
%autosetup -n libnsutils-%{version}

%build
export CFLAGS="%{optflags}"
export LDFLAGS="%{?build_ldflags}"
%make_build PREFIX=%{_prefix} LIBDIR=lib64 NSSHARED=%{_datadir}/netsurf-buildsystem BUILDDIR=build-static
%make_build PREFIX=%{_prefix} LIBDIR=lib64 NSSHARED=%{_datadir}/netsurf-buildsystem BUILDDIR=build-shared COMPONENT_TYPE=lib-shared

%install
make install PREFIX=%{_prefix} LIBDIR=lib64 NSSHARED=%{_datadir}/netsurf-buildsystem BUILDDIR=build-static DESTDIR=%{buildroot}
make install PREFIX=%{_prefix} LIBDIR=lib64 NSSHARED=%{_datadir}/netsurf-buildsystem BUILDDIR=build-shared COMPONENT_TYPE=lib-shared DESTDIR=%{buildroot}
install -d %{buildroot}%{_datadir}/libnsutils/qa
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/libnsutils/qa/libnsutils-%{version}-src.tar.gz

%check
export CFLAGS="%{optflags}"
export LDFLAGS="%{?build_ldflags}"
make test PREFIX=%{_prefix} LIBDIR=lib64 NSSHARED=%{_datadir}/netsurf-buildsystem BUILDDIR=build-static
LD_LIBRARY_PATH="$PWD/build-shared" make test PREFIX=%{_prefix} LIBDIR=lib64 NSSHARED=%{_datadir}/netsurf-buildsystem BUILDDIR=build-shared COMPONENT_TYPE=lib-shared
run_installed_tests() (
    set -eux
    root=$1
    archive="$root/usr/share/libnsutils/qa/libnsutils-0.1.1-src.tar.gz"
    echo '5694b4526e458ed000413ce6027589cbe10a257a7ecf065a01421dc7299dea92  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    tar -xzf "$archive" -C "$work" --strip-components=1
    for header in assert.h errors.h unistd.h endian.h base64.h time.h; do
        cmp -- "$work/include/nsutils/$header" "$root/usr/include/nsutils/$header"
    done
    test "$(grep -Ec '^b64(enctst|dectst|urlenctst|urldectst) ' "$work/test/runtest.sh")" = 32
    mkdir "$work/shared" "$work/static"
    gcc -O2 -g -I"$root/usr/include" "$work/test/base64.c" -L"$root/usr/lib64" -Wl,-rpath,"$root/usr/lib64" -lnsutils -o "$work/shared/test_base64"
    readelf -d "$work/shared/test_base64" | grep 'Shared library: \[libnsutils.so.0\]'
    gcc -O2 -g -I"$root/usr/include" "$work/test/base64.c" "$root/usr/lib64/libnsutils.a" -o "$work/static/test_base64"
    LD_LIBRARY_PATH="$root/usr/lib64" bash -eux "$work/test/runtest.sh" "$work/shared"
    bash -eux "$work/test/runtest.sh" "$work/static"
    echo 'PASS libnsutils unchanged 32-case script against installed shared and static libraries'
)
run_installed_tests '%{buildroot}'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%doc README
%{_libdir}/libnsutils.so.0*

%files devel
%license COPYING
%{_includedir}/nsutils/
%{_libdir}/libnsutils.so
%{_libdir}/libnsutils.a
%{_libdir}/pkgconfig/libnsutils.pc

%files tests
%license COPYING
%{_datadir}/libnsutils/

%changelog
* Mon Oct 19 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 0.1.1-1
- Preserve original static defaults and test script; add shared and installed checks.
