# SPDX-License-Identifier: Apache-2.0

Name:           libfixposix
Version:        0.5.1
Release:        1%{?dist}
Summary:        Thin wrapper providing safer replacements for POSIX functions
License:        BSL-1.0
URL:            https://github.com/sionescu/libfixposix
Source0:        libfixposix-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bats
BuildRequires:  check-devel
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
libfixposix provides consistent, safer wrappers around POSIX interfaces whose
native APIs are difficult to use portably or correctly.

%package devel
Summary:        Development files for libfixposix
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
Headers, linker name, and pkg-config metadata for libfixposix.

%prep
%autosetup -p1

%build
autoreconf -fi
%configure --disable-static --enable-tests
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libfixposix.la

%check
%make_build check

%files
%license LICENCE
%doc README.md
%{_libdir}/libfixposix.so.4*

%files devel
%{_includedir}/lfp.h
%{_includedir}/lfp/
%{_libdir}/libfixposix.so
%{_libdir}/pkgconfig/libfixposix.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.5.1-1
- Initial openEuler RISC-V package with the complete enabled Automake test gate.
