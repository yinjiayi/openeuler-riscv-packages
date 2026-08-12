# SPDX-License-Identifier: Apache-2.0
Name:           graphite2
Version:        1.3.15
Release:        1%{?dist}
Summary:        Smart font rendering engine
License:        LGPL-2.1-or-later OR MPL-2.0 OR GPL-2.0-or-later
URL:            https://graphite.sil.org/
Source0:        graphite2-%{version}.tgz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  python3
BuildRequires:  python3-fonttools

%description
Graphite2 is a rendering engine for fonts that contain Graphite smart-font
tables. It processes language-specific shaping rules while exposing a small
C API.

%package devel
Summary:        Development files for Graphite2
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, the unversioned shared-library link, CMake exports, and pkg-config
metadata for developing applications with Graphite2.

%prep
%autosetup

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_TESTING=ON \
  -DGRAPHITE2_NFILEFACE=OFF \
  -DGRAPHITE2_NTRACING=OFF
%cmake_build

%install
%cmake_install

%check
CTEST_PARALLEL_LEVEL=1 %ctest --timeout 300 --output-on-failure

%files
%license COPYING LICENSE
%doc ChangeLog README.md
%{_bindir}/gr2fonttest
%{_libdir}/libgraphite2.so.3*

%files devel
%license COPYING LICENSE
%{_includedir}/graphite2/
%{_libdir}/libgraphite2.so
%{_libdir}/pkgconfig/graphite2.pc
%{_datadir}/graphite2/

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.15-1
- Initial openEuler RISC-V package with the complete upstream CTest suite.
