# SPDX-License-Identifier: Apache-2.0
Name:           benchmark
Version:        1.9.5
Release:        1%{?dist}
Summary:        Microbenchmark support library
License:        Apache-2.0
URL:            https://github.com/google/benchmark
Source0:        benchmark-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gtest-devel
BuildRequires:  make

%description
Google Benchmark is a C++ library for writing, running, and reporting
microbenchmarks.

%package devel
Summary:        Development files for Google Benchmark
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, CMake metadata, pkg-config files, and unversioned library links for
developing benchmarks.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DGIT_VERSION=%{version} \
  -DBENCHMARK_ENABLE_TESTING=ON \
  -DBENCHMARK_ENABLE_GTEST_TESTS=ON \
  -DBENCHMARK_USE_BUNDLED_GTEST=OFF \
  -DBENCHMARK_DOWNLOAD_DEPENDENCIES=OFF \
  -DBENCHMARK_ENABLE_DOXYGEN=OFF \
  -DBENCHMARK_ENABLE_WERROR=OFF \
  -DBENCHMARK_ENABLE_ASSEMBLY_TESTS=OFF \
  -DBENCHMARK_ENABLE_INSTALL=ON \
  -DBENCHMARK_INSTALL_DOCS=OFF \
  -DBENCHMARK_INSTALL_TOOLS=OFF
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license AUTHORS CONTRIBUTORS LICENSE
%doc README.md
%{_libdir}/libbenchmark.so.1*
%{_libdir}/libbenchmark_main.so.1*

%files devel
%license LICENSE
%{_includedir}/benchmark/
%{_libdir}/libbenchmark.so
%{_libdir}/libbenchmark_main.so
%{_libdir}/cmake/benchmark/
%{_libdir}/pkgconfig/benchmark.pc
%{_libdir}/pkgconfig/benchmark_main.pc

%changelog
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.9.5-1
- Initial openEuler RISC-V package.
