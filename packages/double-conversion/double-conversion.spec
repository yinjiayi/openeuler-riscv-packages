# SPDX-License-Identifier: Apache-2.0
Name:           double-conversion
Version:        3.4.0
Release:        1%{?dist}
Summary:        Binary-decimal floating-point conversion library
License:        BSD-3-Clause
URL:            https://github.com/google/double-conversion
Source0:        double-conversion-%{version}.tar.gz
Patch0:         0001-cmake-support-openeuler-3.27.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make

%description
double-conversion provides efficient, correctly rounded conversion between
binary floating-point values and decimal strings.

%package devel
Summary:        Development files for double-conversion
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config and CMake metadata, and the unversioned library link for
developing applications with double-conversion.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE
%doc AUTHORS Changelog README.md
%{_libdir}/libdouble-conversion.so.3*

%files devel
%license LICENSE
%{_includedir}/double-conversion/
%{_libdir}/libdouble-conversion.so
%{_libdir}/pkgconfig/double-conversion.pc
%{_libdir}/cmake/double-conversion/

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.4.0-1
- Add a build-system-only CMake 3.27 compatibility patch for openEuler.
- Initial openEuler RISC-V package.
