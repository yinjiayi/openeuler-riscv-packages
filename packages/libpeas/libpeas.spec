# SPDX-License-Identifier: Apache-2.0
%global api_version 1.0

Name:           libpeas
Version:        1.36.0
Release:        1%{?dist}
Summary:        GObject-based plug-in engine
License:        LGPL-2.1-or-later
URL:            https://wiki.gnome.org/Projects/Libpeas
Source0:        libpeas-%{version}.tar.xz

BuildRequires:  chrpath
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  gi-docgen
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gladeui-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(pygobject-3.0)
BuildRequires:  python3-devel
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  xorg-x11-xauth
Requires:       python3-gobject

Provides:       %{name}-gtk%{?_isa}
Provides:       %{name}-loader-python3%{?_isa}
Provides:       %{name}-loader-python = %{version}-%{release}

%description
libpeas is a GObject-based plug-in engine that provides applications with
multiple extension points and on-demand language loaders.

%package devel
Summary:        Development files for libpeas
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, linker names, introspection data, documentation, and pkg-config
metadata for applications that use libpeas and its GTK 3 integration.

%prep
%autosetup -p1

%build
%meson \
  -Ddemos=false \
  -Dglade_catalog=true \
  -Dgtk_doc=true \
  -Dintrospection=true \
  -Dpython3=true \
  -Dvapi=true \
  -Dwidgetry=true
%meson_build

%install
%meson_install
chrpath -d %{buildroot}%{_libdir}/libpeas-%{api_version}/loaders/libpython3loader.so
chrpath -d %{buildroot}%{_libdir}/libpeas-gtk-%{api_version}.so
%find_lang libpeas-%{api_version}

%check
xvfb-run -a -s "-screen 0 1024x768x24" \
  meson test -C %{_vpath_builddir} --print-errorlogs

%files -f libpeas-%{api_version}.lang
%license COPYING
%doc AUTHORS NEWS README
%{_libdir}/libpeas-%{api_version}.so.0*
%{_libdir}/libpeas-gtk-%{api_version}.so.0*
%dir %{_libdir}/libpeas-%{api_version}/
%dir %{_libdir}/libpeas-%{api_version}/loaders/
%{_libdir}/libpeas-%{api_version}/loaders/libpython3loader.so
%{_libdir}/girepository-1.0/Peas-%{api_version}.typelib
%{_libdir}/girepository-1.0/PeasGtk-%{api_version}.typelib
%{_datadir}/icons/hicolor/*/actions/libpeas-plugin.*

%files devel
%{_includedir}/libpeas-%{api_version}/
%{_libdir}/libpeas-%{api_version}.so
%{_libdir}/libpeas-gtk-%{api_version}.so
%{_libdir}/pkgconfig/libpeas-%{api_version}.pc
%{_libdir}/pkgconfig/libpeas-gtk-%{api_version}.pc
%{_datadir}/gir-1.0/Peas-%{api_version}.gir
%{_datadir}/gir-1.0/PeasGtk-%{api_version}.gir
%{_datadir}/glade/catalogs/libpeas-gtk.xml
%{_docdir}/libpeas-1.0/
%{_docdir}/libpeas-gtk-1.0/

%changelog
* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.36.0-1
- Package the official GNOME release using the openEuler SP3 feature set.
- Run the complete registered Meson test suite under Xvfb.
