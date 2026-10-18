# SPDX-License-Identifier: Apache-2.0
Name:           libwapcaplet
Version:        0.4.3
Release:        2
Summary:        Reference-counted string internment library
License:        MIT
URL:            https://netsurf-browser.org/projects/libwapcaplet
Source0:        https://download.netsurf-browser.org/libs/releases/libwapcaplet-%{version}-src.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  binutils
BuildRequires:  glibc-devel
BuildRequires:  pkgconfig
BuildRequires:  check-devel >= 0.9.5
BuildRequires:  netsurf-buildsystem >= 1.10
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  which

%description
NetSurf string internment with reference counting and fast caseless comparison.

%package devel
Summary:        Headers, static library and pkg-config metadata for libwapcaplet
Requires:       %{name} = %{version}-%{release}

%description devel
Development files including the original default static library.

%package tests
Summary:        Original libwapcaplet source and installed-library checks
Requires:       %{name}-devel = %{version}-%{release}
Requires:       gcc
Requires:       glibc-devel
Requires:       binutils
Requires:       pkgconfig
Requires:       check-devel >= 0.9.5
Requires:       tar
Requires:       gzip
Requires:       coreutils
Requires:       diffutils

%description tests
Complete original archive for replaying unchanged upstream Check test drivers
against installed shared and static release libraries.

%prep
%autosetup -n libwapcaplet-%{version}

%build
export CFLAGS="%{optflags}"
export LDFLAGS="%{?build_ldflags}"
%make_build PREFIX=%{_prefix} LIBDIR=lib64 NSSHARED=%{_datadir}/netsurf-buildsystem BUILDDIR=build-static
%make_build PREFIX=%{_prefix} LIBDIR=lib64 NSSHARED=%{_datadir}/netsurf-buildsystem BUILDDIR=build-shared COMPONENT_TYPE=lib-shared
# Keep DEBUG/assertion coverage and target fortify hardening together.
%make_build PREFIX=%{_prefix} LIBDIR=lib64 NSSHARED=%{_datadir}/netsurf-buildsystem BUILDDIR=build-debug VARIANT=debug CCNOOPT=-O1

%install
make install PREFIX=%{_prefix} LIBDIR=lib64 NSSHARED=%{_datadir}/netsurf-buildsystem BUILDDIR=build-static DESTDIR=%{buildroot}
make install PREFIX=%{_prefix} LIBDIR=lib64 NSSHARED=%{_datadir}/netsurf-buildsystem BUILDDIR=build-shared COMPONENT_TYPE=lib-shared DESTDIR=%{buildroot}
install -d %{buildroot}%{_datadir}/libwapcaplet/qa
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/libwapcaplet/qa/libwapcaplet-%{version}-src.tar.gz

%check
export CFLAGS="%{optflags}"
export LDFLAGS="%{?build_ldflags}"
make test PREFIX=%{_prefix} LIBDIR=lib64 NSSHARED=%{_datadir}/netsurf-buildsystem BUILDDIR=build-static
LD_LIBRARY_PATH="$PWD/build-shared" make test PREFIX=%{_prefix} LIBDIR=lib64 NSSHARED=%{_datadir}/netsurf-buildsystem BUILDDIR=build-shared COMPONENT_TYPE=lib-shared
make test PREFIX=%{_prefix} LIBDIR=lib64 NSSHARED=%{_datadir}/netsurf-buildsystem BUILDDIR=build-debug VARIANT=debug CCNOOPT=-O1
run_installed_tests() (
    set -eux
    root=$1
    archive="$root/usr/share/libwapcaplet/qa/libwapcaplet-0.4.3-src.tar.gz"
    echo '9b2aa1dd6d6645f8e992b3697fdbd87f0c0e1da5721fa54ed29b484d13160c5c  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    tar -xzf "$archive" -C "$work" --strip-components=1
    cmp -- "$work/include/libwapcaplet/libwapcaplet.h" "$root/usr/include/libwapcaplet/libwapcaplet.h"
    # Match the installed upstream-default release library; debug tests run separately.
    gcc -O2 -g -DNDEBUG -I"$root/usr/include" $(pkg-config --cflags check) "$work/test/testmain.c" "$work/test/basictests.c" -L"$root/usr/lib64" -Wl,-rpath,"$root/usr/lib64" -lwapcaplet $(pkg-config --libs check) -o "$work/shared-tests"
    readelf -d "$work/shared-tests" | grep 'Shared library: \[libwapcaplet.so.0\]'
    gcc -O2 -g -DNDEBUG -I"$root/usr/include" $(pkg-config --cflags check) "$work/test/testmain.c" "$work/test/basictests.c" "$root/usr/lib64/libwapcaplet.a" $(pkg-config --libs check) -o "$work/static-tests"
    LD_LIBRARY_PATH="$root/usr/lib64" "$work/shared-tests"
    "$work/static-tests"
    echo 'PASS libwapcaplet unchanged upstream release suite against installed shared and static libraries'
)
run_installed_tests '%{buildroot}'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%doc README
%{_libdir}/libwapcaplet.so.0*

%files devel
%license COPYING
%{_includedir}/libwapcaplet/
%{_libdir}/libwapcaplet.so
%{_libdir}/libwapcaplet.a
%{_libdir}/pkgconfig/libwapcaplet.pc

%files tests
%license COPYING
%{_datadir}/libwapcaplet/

%changelog
* Mon Oct 19 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 0.4.3-2
- Use O1 only for additional debug builds to retain target fortify and assertions.

* Mon Oct 19 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 0.4.3-1
- Preserve static release defaults and original tests; add shared/debug/installed checks.
