# SPDX-License-Identifier: Apache-2.0
Name:           rofi-reddit
Version:        0.1.2
Release:        1%{?dist}
Summary:        Browse reddit threads from rofi using the Reddit API
License:        GPL-3.0-or-later
URL:            https://github.com/valdebrutal/rofi-reddit
Source0:        rofi-reddit-0.1.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Browse reddit threads from rofi using the Reddit API

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

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.2-1
- Initial openEuler RISC-V package from the full package inventory.
