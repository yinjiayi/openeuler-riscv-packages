# SPDX-License-Identifier: Apache-2.0
Name:           gtest
Version:        1.17.0
Release:        1%{?dist}
Summary:        Google C++ testing and mocking framework
License:        BSD-3-Clause
URL:            https://github.com/google/googletest
Source0:        gtest-1.17.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make


%description
GoogleTest is a C++ testing framework with GoogleMock support.

%package devel
Summary:        Development files for GoogleTest
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, libraries, pkg-config files, and CMake metadata for GoogleTest.

%prep
%autosetup -p1 -n googletest-%{version}

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -Dgtest_build_samples=ON \
  -Dgtest_build_tests=OFF
%cmake_build

%install
%cmake_install

%check
for sample in \
  sample1_unittest sample2_unittest sample3_unittest sample4_unittest \
  sample5_unittest sample6_unittest sample7_unittest sample8_unittest \
  sample9_unittest sample10_unittest
do
  "%{_vpath_builddir}/googletest/${sample}"
done

%files
%license LICENSE
%doc README.md
%{_libdir}/libgtest.so.1*
%{_libdir}/libgtest_main.so.1*
%{_libdir}/libgmock.so.1*
%{_libdir}/libgmock_main.so.1*

%files devel
%license LICENSE
%{_includedir}/gtest/
%{_includedir}/gmock/
%{_libdir}/libgtest.so
%{_libdir}/libgtest_main.so
%{_libdir}/libgmock.so
%{_libdir}/libgmock_main.so
%{_libdir}/cmake/GTest/
%{_libdir}/pkgconfig/gtest.pc
%{_libdir}/pkgconfig/gtest_main.pc
%{_libdir}/pkgconfig/gmock.pc
%{_libdir}/pkgconfig/gmock_main.pc

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.17.0-1
- Initial openEuler RISC-V package.
