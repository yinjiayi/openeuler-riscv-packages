# SPDX-License-Identifier: Apache-2.0
Name:           libasyncns
Version:        0.8
Release:        1%{?dist}
Summary:        Asynchronous name service query library
License:        LGPL-2.1-or-later
URL:            https://0pointer.net/lennart/projects/libasyncns/
Source0:        libasyncns-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
libasyncns is a small C library that executes name-service queries
asynchronously using worker threads or processes.

%package devel
Summary:        Development files for libasyncns
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
Headers, pkg-config metadata, and the unversioned linker name for developing
applications with libasyncns.

%prep
%autosetup -p1

%build
%configure \
  --disable-static \
  --enable-shared
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
# The upstream target builds its asynchronous-query test program.
%make_build check

%files
%license LICENSE
%doc README doc/README.html doc/style.css
%{_libdir}/libasyncns.so.0*

%files devel
%license LICENSE
%{_includedir}/asyncns.h
%{_libdir}/libasyncns.so
%{_libdir}/pkgconfig/libasyncns.pc

%changelog
* Fri Aug 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8-1
- Package the official stable libasyncns release for RVA23.
- Preserve the upstream check target and add an installed API smoke test.
