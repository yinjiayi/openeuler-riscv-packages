# SPDX-License-Identifier: Apache-2.0
Name:           SFML
Version:        2.6.2
Release:        1%{?dist}
Summary:        Simple and Fast Multimedia Library 2.x compatibility stack
License:        Zlib AND Apache-2.0 AND CC0-1.0 AND MIT AND (MIT AND Apache-2.0) AND (MIT OR Unlicense) AND LicenseRef-Public-Domain
URL:            https://www.sfml-dev.org/
Source0:        SFML-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  flac-devel
BuildRequires:  freetype-devel
BuildRequires:  gcc-c++
BuildRequires:  libX11-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libogg-devel
BuildRequires:  libvorbis-devel
BuildRequires:  make
BuildRequires:  mesa-libGL-devel
BuildRequires:  openal-soft-devel
BuildRequires:  systemd-devel
Provides:       sfml2 = %{version}-%{release}

%description
SFML is a portable C++ multimedia API made of System, Window, Graphics, Audio,
and Network modules. This package preserves the stable 2.x API and ABI for
applications that have not migrated to SFML 3.

%package devel
Summary:        Development files for SFML 2.x
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       cmake
Provides:       sfml2-devel = %{version}-%{release}

%description devel
Headers, unversioned shared-library links, CMake package metadata, and
pkg-config metadata for developing applications against SFML 2.x.

%prep
%autosetup -p1 -n SFML-%{version}

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DSFML_BUILD_AUDIO=ON \
  -DSFML_BUILD_EXAMPLES=OFF \
  -DSFML_BUILD_GRAPHICS=ON \
  -DSFML_BUILD_NETWORK=ON \
  -DSFML_BUILD_TEST_SUITE=ON \
  -DSFML_BUILD_WINDOW=ON \
  -DSFML_USE_SYSTEM_DEPS=ON
%cmake_build

%install
%cmake_install

%check
%ctest --output-on-failure

%files
%doc %{_docdir}/SFML/readme.md
%license %{_docdir}/SFML/license.md
%{_libdir}/libsfml-*.so.2*

%files devel
%{_includedir}/SFML/
%{_libdir}/cmake/SFML/
%{_libdir}/libsfml-*.so
%{_libdir}/pkgconfig/sfml-*.pc

%changelog
* Sun Sep 06 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.6.2-1
- Initial SFML 2.x compatibility package from frozen cross-distribution evidence.
