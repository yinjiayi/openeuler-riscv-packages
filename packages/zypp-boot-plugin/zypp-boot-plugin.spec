# SPDX-License-Identifier: Apache-2.0
Name:           zypp-boot-plugin
Version:        0.0.13
Release:        1%{?dist}
Summary:        Zypp plugin for checking if a reboot is needed
License:        GPL-3.0-or-later
URL:            https://github.com/openSUSE/zypp-boot-plugin
Source0:        zypp-boot-plugin-0.0.13.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Zypp plugin for checking if a reboot is needed

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
%license LICENSE
%doc README.md
%doc NEWS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.13-1
- Initial openEuler RISC-V package from the full package inventory.
