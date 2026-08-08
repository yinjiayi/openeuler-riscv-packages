# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           argparse
Version:        3.2
Release:        1%{?dist}
Summary:        Header-only argument parser for modern C++
License:        MIT
URL:            https://github.com/p-ranav/argparse
Source0:        argparse-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make

%description
argparse is a single-header C++17 command-line argument parser modeled after
Python's argparse module. The package also installs CMake and pkg-config
metadata.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DARGPARSE_INSTALL=ON \
  -DARGPARSE_BUILD_TESTS=ON \
  -DARGPARSE_BUILD_SAMPLES=OFF
%cmake_build

%install
%cmake_install

%check
"%{_vpath_builddir}/test/tests"

%files
%license LICENSE
%doc README.md
%{_includedir}/argparse/
%{_libdir}/cmake/argparse/
%{_libdir}/pkgconfig/argparse.pc

%changelog
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2-1
- Initial openEuler RISC-V package.
