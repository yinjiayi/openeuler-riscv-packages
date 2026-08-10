# SPDX-License-Identifier: Apache-2.0
Name:           pugixml
Version:        1.16
Release:        1%{?dist}
Summary:        Lightweight C++ XML parser with XPath support
License:        MIT
URL:            https://pugixml.org
Source0:        pugixml-1.16.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make


%description
pugixml is a lightweight C++ XML parser with XPath support.

%package devel
Summary:        Development files for pugixml
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and CMake integration for pugixml.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DPUGIXML_BUILD_TESTS=ON
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE.md
%doc README.md
%{_libdir}/libpugixml.so.1*

%files devel
%license LICENSE.md
%{_includedir}/pugiconfig.hpp
%{_includedir}/pugixml.hpp
%{_libdir}/libpugixml.so
%{_libdir}/cmake/pugixml/
%{_libdir}/pkgconfig/pugixml.pc

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.16-1
- Initial openEuler RISC-V package.
