# SPDX-License-Identifier: Apache-2.0
Name:           muffin
Version:        6.6.3
Release:        1%{?dist}
Summary:        Cinnamon window manager based on Mutter
License:        GPL-2.0-or-later
URL:            https://github.com/linuxmint/muffin
Source0:        muffin-6.6.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Cinnamon window manager based on Mutter

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.6.3-1
- Initial openEuler RISC-V package from the full package inventory.
