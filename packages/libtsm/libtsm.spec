# SPDX-License-Identifier: Apache-2.0
Name:           libtsm
Version:        4.7.1
Release:        1%{?dist}
Summary:        Terminal-emulator state machine library
License:        MIT AND LGPL-2.1-or-later
URL:            https://github.com/kmscon/libtsm
Source0:        v4.7.1.tar.gz

BuildRequires:  check-devel
BuildRequires:  gcc
BuildRequires:  libxkbcommon-devel
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf

%description
libtsm provides a terminal-emulator state machine, including screen and VTE
implementations, for applications that need an embeddable terminal model.

%package devel
Summary:        Development files for libtsm
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, pkg-config metadata, and the unversioned linker name for developing
applications with libtsm.

%prep
%autosetup -p1

%build
%meson -Dtests=true -Dgtktsm=false
%meson_build

%install
%meson_install

%check
%meson_test

%files
%license COPYING LICENSE_htable
%doc NEWS.md README.md
%{_libdir}/libtsm.so.4*

%files devel
%license COPYING LICENSE_htable
%{_includedir}/libtsm.h
%{_libdir}/libtsm.so
%{_libdir}/pkgconfig/libtsm.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.7.0-1
- Initial openEuler RISC-V package with all seven upstream Meson tests.
