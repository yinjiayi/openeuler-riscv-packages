# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           variant-lite
Version:        3.0.0
Release:        1%{?dist}
Summary:        C++17-like variant for C++98, C++11 and later
License:        BSL-1.0
URL:            https://github.com/nonstd-lite/variant-lite
Source0:        variant-lite-3.0.0.tar.gz
BuildArch:      noarch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make

%description
variant-lite provides a C++17-like type-safe union for C++98, C++11 and later
as a single-file header-only library, with CMake package integration.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DVARIANT_LITE_OPT_BUILD_TESTS=ON \
  -DVARIANT_LITE_OPT_BUILD_EXAMPLES=OFF \
  -DVARIANT_LITE_OPT_SELECT_NONSTD=ON \
  -DVARIANT_LITE_OPT_SELECT_STD=OFF
%cmake_build

%install
%cmake_install

%check
ctest --test-dir %{_vpath_builddir} \
  --output-on-failure --force-new-ctest-process -j1

%files
%license LICENSE.txt
%doc README.md
%{_includedir}/nonstd/
%{_libdir}/cmake/variant-lite/

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.0-1
- Initial openEuler RISC-V package with the upstream CTest suite.
