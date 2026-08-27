# SPDX-License-Identifier: Apache-2.0
Name:           waybox
Version:        0.2.2
Release:        1%{?dist}
Summary:        Openbox clone on Wayland
License:        MIT
URL:            https://github.com/wizbright/waybox
Source0:        waybox-0.2.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Openbox clone on Wayland

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.2-1
- Initial openEuler RISC-V package from the full package inventory.
