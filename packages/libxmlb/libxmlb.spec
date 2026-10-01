# SPDX-License-Identifier: Apache-2.0
Name:           libxmlb
Version:        0.3.29
Release:        1%{?dist}
Summary:        Fast indexed binary representation of XML metadata
License:        LGPL-2.1-or-later
URL:            https://github.com/hughsie/libxmlb
Source0:        libxmlb-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  glib2-devel >= 2.56
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk-doc
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf-pkg-config
BuildRequires:  python3
BuildRequires:  shared-mime-info
BuildRequires:  xz-devel
BuildRequires:  zstd-devel
Requires:       shared-mime-info

%description
Libxmlb turns XML metadata into a binary form optimized for indexed queries.
The package includes the xb-tool compiler and query utility.

%package devel
Summary:        Development files for libxmlb
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       glib2-devel%{?_isa}
Requires:       pkgconf-pkg-config

%description devel
Public headers, GObject Introspection data, pkg-config metadata, and gtk-doc
reference files for applications using libxmlb.

%package tests
Summary:        Installed upstream tests for libxmlb
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tests
The upstream installed self-test binary and its fixture data.

%prep
%autosetup -p1

%build
%meson \
  -Dcli=true \
  -Dintrospection=true \
  -Dgtkdoc=true \
  -Dtests=true \
  -Dlzma=enabled \
  -Dzstd=enabled
%meson_build

%install
%meson_install

%check
%meson_test

%files
%license LICENSE
%doc README.md
%{_bindir}/xb-tool
%{_mandir}/man1/xb-tool.1*
%{_libdir}/libxmlb.so.2*
%{_libdir}/girepository-1.0/Xmlb-2.0.typelib

%files devel
%license LICENSE
%{_includedir}/libxmlb-2/
%{_libdir}/libxmlb.so
%{_libdir}/pkgconfig/xmlb.pc
%{_datadir}/gir-1.0/Xmlb-2.0.gir
%{_datadir}/gtk-doc/html/libxmlb/

%files tests
%license LICENSE
%{_libexecdir}/installed-tests/libxmlb/
%{_datadir}/installed-tests/libxmlb/

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.29-1
- Package the official libxmlb 0.3.29 release for openEuler RISC-V.
