# SPDX-License-Identifier: Apache-2.0
Name:           xviewer-plugins
Version:        3.4.3
Release:        1%{?dist}
Summary:        Plugins for xviewer. X-Apps Project.
License:        GPL-2.0-or-later
URL:            https://github.com/linuxmint/xviewer-plugins
Source0:        xviewer-plugins-3.4.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Plugins for xviewer. X-Apps Project.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.4.3-1
- Initial openEuler RISC-V package from the full package inventory.
