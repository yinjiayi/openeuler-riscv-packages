# SPDX-License-Identifier: Apache-2.0
Name:           lunar-calendar
Version:        3.0.1
Release:        1%{?dist}
Summary:        a gtk+ calendar widget for chinese lunar library.
License:        LGPL-2.1-or-later
URL:            https://github.com/yetist/lunar-calendar
Source0:        lunar-calendar-3.0.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
a gtk+ calendar widget for chinese lunar library.

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
%doc README.md
%doc NEWS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.1-1
- Initial openEuler RISC-V package from the full package inventory.
