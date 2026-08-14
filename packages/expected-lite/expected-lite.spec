# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           expected-lite
Version:        0.10.0
Release:        1%{?dist}
Summary:        C++11 expected objects in a single-file header-only library
License:        BSL-1.0
URL:            https://github.com/nonstd-lite/expected-lite
Source0:        expected-lite-0.10.0.tar.gz
BuildArch:      noarch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make

%description
expected-lite provides expected and unexpected objects for C++11 and later as
a single-file header-only library, with CMake package integration.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DEXPECTED_LITE_OPT_BUILD_TESTS=ON \
  -DEXPECTED_LITE_OPT_BUILD_EXAMPLES=OFF \
  -DEXPECTED_LITE_OPT_SELECT_NONSTD=ON \
  -DEXPECTED_LITE_OPT_SELECT_STD=OFF
%cmake_build

%install
%cmake_install

%check
ctest --test-dir %{_vpath_builddir} \
  --output-on-failure --force-new-ctest-process -j1

%files
%license LICENSE.txt
%doc CHANGES.txt Notes.md README.md
%{_includedir}/nonstd/
%{_libdir}/cmake/expected-lite/

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.10.0-1
- Initial openEuler RISC-V package with the upstream CTest suite.
