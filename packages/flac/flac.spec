# SPDX-License-Identifier: Apache-2.0
Name:           flac
Version:        1.5.0
Release:        1%{?dist}
Summary:        Free Lossless Audio Codec reference implementation
License:        BSD-3-Clause AND GPL-2.0-or-later AND GFDL-1.3-or-later
URL:            https://xiph.org/flac/
Source0:        flac-%{version}.tar.xz

BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gettext-devel
BuildRequires:  libogg-devel
BuildRequires:  make

%description
FLAC is a lossless audio format and reference implementation. This package
contains the command-line tools and the C and C++ runtime libraries.

%package devel
Summary:        Development files for FLAC
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libogg-devel

%description devel
Headers, unversioned library links, CMake files, pkg-config metadata, and
Autoconf macros for developing applications with FLAC.

%package help
Summary:        Documentation for FLAC
BuildArch:      noarch

%description help
Command manual pages and generated API documentation for FLAC.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_CXXLIBS=ON \
  -DBUILD_DOCS=ON \
  -DBUILD_DOXYGEN=ON \
  -DBUILD_EXAMPLES=ON \
  -DBUILD_PROGRAMS=ON \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_TESTING=ON \
  -DINSTALL_CMAKE_CONFIG_MODULE=ON \
  -DINSTALL_MANPAGES=ON \
  -DINSTALL_PKGCONFIG_MODULES=ON \
  -DWITH_OGG=ON
%cmake_build

%install
%cmake_install
mkdir -p %{buildroot}%{_datadir}/aclocal
install -pm 0644 src/libFLAC/libFLAC.m4 %{buildroot}%{_datadir}/aclocal/
install -pm 0644 src/libFLAC++/libFLAC++.m4 %{buildroot}%{_datadir}/aclocal/

%check
%ctest --parallel 1

%files
%license COPYING.Xiph COPYING.GPL COPYING.LGPL
%{_bindir}/flac
%{_bindir}/metaflac
%{_libdir}/libFLAC.so.14*
%{_libdir}/libFLAC++.so.11*

%files devel
%license COPYING.Xiph
%{_includedir}/FLAC/
%{_includedir}/FLAC++/
%{_libdir}/libFLAC.so
%{_libdir}/libFLAC++.so
%{_libdir}/pkgconfig/flac.pc
%{_libdir}/pkgconfig/flac++.pc
%{_libdir}/cmake/FLAC/
%{_datadir}/aclocal/libFLAC.m4
%{_datadir}/aclocal/libFLAC++.m4

%files help
%license COPYING.Xiph COPYING.GPL COPYING.FDL
%doc AUTHORS README.md CHANGELOG.md
%{_docdir}/FLAC/api/
%{_mandir}/man1/flac.1*
%{_mandir}/man1/metaflac.1*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.0-1
- Pass the serial CTest setting through the openEuler RPM macro.
- Initial openEuler RISC-V package from reviewed Fedora 44 and upstream evidence.
