# SPDX-License-Identifier: Apache-2.0
Name:           pixman
Version:        0.46.4
Release:        1%{?dist}
Summary:        Pixel manipulation library
License:        MIT
URL:            https://www.pixman.org/
Source0:        pixman-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  libpng-devel
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Pixman is a low-level software library for pixel manipulation, including
image compositing and trapezoid rasterization.

%package devel
Summary:        Development files for pixman
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, the unversioned shared-library link, and pkg-config metadata for
developing applications with pixman.

%prep
%autosetup

%build
%meson \
  -Ddemos=disabled \
  -Dgtk=disabled \
  -Dlibpng=enabled \
  -Dtests=enabled
%meson_build

%install
%meson_install

%check
%meson_test

%files
%license COPYING
%doc AUTHORS NEWS README
%{_libdir}/libpixman-1.so.0*

%files devel
%license COPYING
%{_includedir}/pixman-1/
%{_libdir}/libpixman-1.so
%{_libdir}/pkgconfig/pixman-1.pc

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.46.4-1
- Initial openEuler RISC-V package from Fedora 44 and cross-distribution evidence.
