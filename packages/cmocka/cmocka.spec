# SPDX-License-Identifier: Apache-2.0
Name:           cmocka
Version:        2.0.2
Release:        1%{?dist}
Summary:        Unit testing framework for C with mock object support
License:        Apache-2.0
URL:            https://cmocka.org
Source0:        cmocka-2.0.2.tar.xz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
Unit testing framework for C with mock object support.

%package -n libcmocka
Summary:        Shared library for the cmocka unit testing framework

%description -n libcmocka
The runtime shared library for cmocka.

%package -n libcmocka-devel
Summary:        Development files for cmocka
Requires:       libcmocka%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description -n libcmocka-devel
Headers, pkg-config metadata, and CMake targets for cmocka applications.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DWITH_STATIC_LIB=OFF \
  -DUNIT_TESTING=ON \
  -DWITH_EXAMPLES=OFF \
  -DWITH_DOC=OFF
%cmake_build

%install
%cmake_install

%check
%ctest --output-on-failure --parallel 1

%ldconfig_scriptlets -n libcmocka

%files

%files -n libcmocka
%license LICENSE
%doc AUTHORS README.md CHANGELOG.md
%{_libdir}/libcmocka.so.*

%files -n libcmocka-devel
%{_includedir}/cmocka.h
%{_includedir}/cmocka_pbc.h
%{_includedir}/cmocka_version.h
%{_libdir}/libcmocka.so
%{_libdir}/pkgconfig/cmocka.pc
%{_libdir}/cmake/cmocka/

%changelog
* Sun Aug 16 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.2-1
- Package cmocka with its shared library, development files, and full CTest suite.
