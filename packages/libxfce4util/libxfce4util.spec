# SPDX-License-Identifier: Apache-2.0
Name:           libxfce4util
Version:        4.20.1
Release:        1%{?dist}
Summary:        Utility library for the Xfce desktop environment
License:        LGPL-2.0-or-later AND GPL-2.0-or-later
URL:            https://docs.xfce.org/xfce/libxfce4util/start
Source0:        libxfce4util-4.20.1.tar.bz2
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(gio-2.0) >= 2.72.0
BuildRequires:  pkgconfig(glib-2.0) >= 2.72.0
BuildRequires:  pkgconfig(gobject-2.0) >= 2.72.0
BuildRequires:  pkgconfig(gobject-introspection-1.0) >= 1.72.0
BuildRequires:  python3
BuildRequires:  vala

%description
Library of non-GUI utility functions shared by applications in the Xfce
desktop environment.

%prep
%autosetup -p1

%build
%meson \
  -Dintrospection=true \
  -Dvala=enabled
%meson_build

%install
%meson_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%meson_test
%{_vpath_builddir}/xfce4-kiosk-query/xfce4-kiosk-query -v

%files -f %{name}.files
%license COPYING
%doc AUTHORS
%doc ChangeLog
%doc NEWS
%doc README.md

%changelog
* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.20.1-1
- Initial openEuler RISC-V package from the full package inventory.
