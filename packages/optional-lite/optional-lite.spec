# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           optional-lite
Version:        3.6.0
Release:        1%{?dist}
Summary:        C++ optional for C++98, C++11 and later
License:        BSL-1.0
URL:            https://github.com/nonstd-lite/optional-lite
Source0:        optional-lite-3.6.0.tar.gz
BuildArch:      noarch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make

%description
optional-lite provides a C++17-like optional type for C++98, C++11 and later
as a single-file header-only library, with CMake package integration.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DOPTIONAL_LITE_OPT_BUILD_TESTS=ON \
  -DOPTIONAL_LITE_OPT_BUILD_EXAMPLES=OFF \
  -DOPTIONAL_LITE_OPT_SELECT_NONSTD=ON \
  -DOPTIONAL_LITE_OPT_SELECT_STD=OFF
%cmake_build

%install
%cmake_install

%check
ctest --test-dir %{_vpath_builddir} \
  --output-on-failure --force-new-ctest-process -j1

%files
%license LICENSE.txt
%doc CHANGES.txt README.md
%{_includedir}/nonstd/
%{_libdir}/cmake/optional-lite/

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.6.0-1
- Initial openEuler RISC-V package with the upstream CTest suite.
