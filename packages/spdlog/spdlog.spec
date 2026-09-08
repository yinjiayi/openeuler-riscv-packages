# SPDX-License-Identifier: Apache-2.0
Name:           spdlog
Version:        1.17.0
Release:        1%{?dist}
Summary:        Fast C++ logging library
License:        MIT
URL:            https://github.com/gabime/spdlog
Source0:        spdlog-1.17.0.tar.gz
Source1:        catch2-3.5.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make


%description
spdlog is a fast C++ logging library with both compiled and header-only APIs.

%package devel
Summary:        Development files for spdlog
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and CMake integration for spdlog.

%prep
%autosetup -p1 -a 1

%build
%cmake_conf \
  -DSPDLOG_BUILD_EXAMPLE=OFF \
  -DSPDLOG_BUILD_SHARED=ON \
  -DSPDLOG_BUILD_TESTS=ON \
  -DSPDLOG_FMT_EXTERNAL=OFF \
  -DFETCHCONTENT_SOURCE_DIR_CATCH2="$PWD/Catch2-3.5.0"
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE
%doc README.md
%{_libdir}/libspdlog.so.1*

%files devel
%license LICENSE
%{_includedir}/spdlog/
%{_libdir}/libspdlog.so
%{_libdir}/cmake/spdlog/
%{_libdir}/pkgconfig/spdlog.pc

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.17.0-1
- Initial openEuler RISC-V package.
