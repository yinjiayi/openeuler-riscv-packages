# SPDX-License-Identifier: Apache-2.0
%undefine _debugsource_packages

Name:           catch2
Version:        3.15.3
Release:        1%{?dist}
Summary:        Modern C++ test framework for unit tests, TDD, and BDD
License:        BSL-1.0
URL:            https://github.com/catchorg/Catch2
Source0:        catch2-3.15.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  python3


%description
Catch2 is a modern C++ testing framework for unit tests, test-driven
development, and behavior-driven development.

%package devel
Summary:        Development files for Catch2
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, CMake integration, pkg-config metadata, and link libraries for Catch2.

%prep
%autosetup -p1 -n Catch2-%{version}

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DCATCH_DEVELOPMENT_BUILD=ON \
  -DCATCH_ENABLE_WERROR=OFF \
  -DCATCH_INSTALL_DOCS=OFF \
  -DCATCH_INSTALL_EXTRAS=OFF
%cmake_build

%install
%cmake_install

%check
%ctest -- -j1

%files
%license LICENSE.txt
%doc README.md
%{_libdir}/libCatch2.so.3*
%{_libdir}/libCatch2Main.so.3*

%files devel
%license LICENSE.txt
%{_includedir}/catch2/
%{_libdir}/libCatch2.so
%{_libdir}/libCatch2Main.so
%{_libdir}/cmake/Catch2/
%{_datadir}/pkgconfig/catch2.pc
%{_datadir}/pkgconfig/catch2-with-main.pc

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.15.3-1
- Initial openEuler RISC-V package.
