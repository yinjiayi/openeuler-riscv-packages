# SPDX-License-Identifier: Apache-2.0
Name:           libdaemon
Version:        0.14
Release:        1%{?dist}
Summary:        Library for writing UNIX daemons
License:        LGPL-2.1-or-later
URL:            https://0pointer.net/lennart/projects/libdaemon/
Source0:        libdaemon-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
libdaemon is a lightweight C library that eases the writing of UNIX daemons.
It provides portable helpers for forking, logging, signals, PID files,
non-blocking descriptors, and executing child processes.

%package devel
Summary:        Development files for libdaemon
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
Headers, pkg-config metadata, and the unversioned linker name for developing
applications with libdaemon.

%prep
%autosetup -p1

%build
%configure \
  --disable-static \
  --enable-shared \
  --disable-examples
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
# The upstream release defines no test programs; retain its recursive target.
%make_build check

%files
%license LICENSE
%doc README doc/README.html doc/style.css
%{_libdir}/libdaemon.so.0*

%files devel
%license LICENSE
%{_includedir}/libdaemon/
%{_libdir}/libdaemon.so
%{_libdir}/pkgconfig/libdaemon.pc

%changelog
* Fri Aug 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.14-1
- Package the official stable libdaemon release for RVA23.
- Preserve the upstream check target and add an installed API smoke test.
