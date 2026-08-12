# SPDX-License-Identifier: Apache-2.0
%global upstream_commit 613debeaea72ee66626dace9ba1a2eff11b5d37d
%global library_version 8.0.2

Name:           qhull
Version:        2020.2
Release:        2%{?dist}
Summary:        Compute convex hulls and related geometric structures
License:        LicenseRef-qhull
URL:            http://www.qhull.org/
Source0:        qhull-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Qhull computes convex hulls, Delaunay triangulations, Voronoi diagrams,
furthest-site Voronoi diagrams, and halfspace intersections in arbitrary
dimensions.

%package devel
Summary:        Development files for Qhull
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, static libraries, CMake and pkg-config metadata, and unversioned
linker names for developing applications with Qhull.

%package help
Summary:        Documentation for Qhull
BuildArch:      noarch

%description help
Qhull command manual pages and upstream HTML documentation.

%prep
%autosetup -n qhull-%{upstream_commit} -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_STATIC_LIBS=ON \
  -DLINK_APPS_SHARED=ON \
  -DLIB_INSTALL_DIR=%{_lib}
%cmake_build
# These deprecated shared targets remain part of the target ABI and must be
# built explicitly because upstream excludes them from its default target.
%cmake_build --target libqhull qhull_p

%install
%cmake_install
mv %{buildroot}%{_prefix}/lib/pkgconfig \
  %{buildroot}%{_libdir}/pkgconfig
install -p -m 0755 %{_vpath_builddir}/libqhull.so.%{library_version} \
  %{buildroot}%{_libdir}/libqhull.so.%{library_version}
ln -s libqhull.so.%{library_version} \
  %{buildroot}%{_libdir}/libqhull.so.8.0
ln -s libqhull.so.8.0 %{buildroot}%{_libdir}/libqhull.so
install -p -m 0755 %{_vpath_builddir}/libqhull_p.so.%{library_version} \
  %{buildroot}%{_libdir}/libqhull_p.so.%{library_version}
ln -s libqhull_p.so.%{library_version} \
  %{buildroot}%{_libdir}/libqhull_p.so.8.0
ln -s libqhull_p.so.8.0 %{buildroot}%{_libdir}/libqhull_p.so

%check
%ctest -- -j1

%files
%license COPYING.txt
%{_bindir}/qconvex
%{_bindir}/qdelaunay
%{_bindir}/qhalf
%{_bindir}/qhull
%{_bindir}/qvoronoi
%{_bindir}/rbox
%{_libdir}/libqhull.so.8*
%{_libdir}/libqhull_p.so.8*
%{_libdir}/libqhull_r.so.8*

%files devel
%license COPYING.txt
%{_includedir}/libqhull/
%{_includedir}/libqhull_r/
%{_includedir}/libqhullcpp/
%{_libdir}/libqhull.so
%{_libdir}/libqhull_p.so
%{_libdir}/libqhull_r.so
%{_libdir}/libqhullcpp.a
%{_libdir}/libqhullstatic.a
%{_libdir}/libqhullstatic_r.a
%{_prefix}/lib/cmake/Qhull/
%{_libdir}/pkgconfig/qhull_r.pc
%{_libdir}/pkgconfig/qhullcpp.pc
%{_libdir}/pkgconfig/qhullstatic.pc
%{_libdir}/pkgconfig/qhullstatic_r.pc

%files help
%license COPYING.txt
%{_mandir}/man1/qhull.1*
%{_mandir}/man1/rbox.1*
%{_docdir}/qhull/

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2020.2-2
- Rebuild Qhull for openEuler RISC-V from Fedora 44 and frozen cross-distribution evidence.
- Preserve the target's deprecated libqhull and libqhull_p ABI compatibility libraries.
