# SPDX-License-Identifier: Apache-2.0
Name:           uchardet
Version:        0.0.8
Release:        1%{?dist}
Summary:        Universal character encoding detector
License:        MPL-1.1 OR GPL-2.0-or-later OR LGPL-2.0-or-later
URL:            https://www.freedesktop.org/wiki/Software/uchardet/
Source0:        uchardet-%{version}.tar.xz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Uchardet is an encoding detector library and command-line tool derived from
Mozilla's universal character set detector.

%package devel
Summary:        Development files for uchardet
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, the unversioned shared-library link, CMake metadata, and pkg-config
metadata for developing applications with uchardet.

%prep
%autosetup

%build
%cmake \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_STATIC=OFF \
  -DCMAKE_INSTALL_LIBDIR=%{_libdir}
%cmake_build

%install
%cmake_install

%check
%ctest --output-on-failure --parallel 1

%files
%license COPYING
%doc AUTHORS README.md
%{_bindir}/uchardet
%{_libdir}/libuchardet.so.*
%{_mandir}/man1/uchardet.1*

%files devel
%license COPYING
%{_includedir}/uchardet/
%{_libdir}/cmake/uchardet/
%{_libdir}/libuchardet.so
%{_libdir}/pkgconfig/uchardet.pc

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.8-1
- Initial openEuler RISC-V package from Fedora 44 and cross-distribution evidence.
