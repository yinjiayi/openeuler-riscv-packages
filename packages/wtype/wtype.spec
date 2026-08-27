# SPDX-License-Identifier: Apache-2.0
Name:           wtype
Version:        0.4
Release:        1%{?dist}
Summary:        xdotool type for wayland
License:        MIT
URL:            https://github.com/atx/wtype
Source0:        wtype-0.4.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
xdotool type for wayland

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4-1
- Initial openEuler RISC-V package from the full package inventory.
