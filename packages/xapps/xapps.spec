# SPDX-License-Identifier: Apache-2.0
Name:           xapps
Version:        3.2.2
Release:        1%{?dist}
Summary:        Common files for XApp desktop apps
License:        LGPL-3.0-or-later
URL:            https://github.com/linuxmint/xapps
Source0:        xapps-3.2.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Common files for XApp desktop apps

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%meson_test

%files -f %{name}.files
%license COPYING
%license COPYING.LESSER
%doc README.md
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2.2-1
- Initial openEuler RISC-V package from the full package inventory.
