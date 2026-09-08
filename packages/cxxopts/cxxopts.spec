# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           cxxopts
Version:        3.3.1
Release:        1%{?dist}
Summary:        Lightweight header-only C++ command-line option parser
License:        MIT AND BSL-1.0
URL:            https://github.com/jarro2783/cxxopts
Source0:        cxxopts-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make

%description
cxxopts is a lightweight header-only C++ library for parsing command-line
options with a GNU-style interface.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DCXXOPTS_BUILD_EXAMPLES=ON \
  -DCXXOPTS_BUILD_TESTS=ON \
  -DCXXOPTS_ENABLE_INSTALL=ON
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE
%doc CHANGELOG.md README.md
%{_includedir}/cxxopts.hpp
%{_datadir}/cmake/cxxopts/
%{_datadir}/pkgconfig/cxxopts.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.3.1-1
- Initial openEuler RISC-V package with all upstream integration tests.
