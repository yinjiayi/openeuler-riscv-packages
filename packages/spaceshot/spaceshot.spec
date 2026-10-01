# SPDX-License-Identifier: Apache-2.0
Name:           spaceshot
Version:        0.6.2
Release:        1%{?dist}
Summary:        A batteries-included screenshot tool for wlroots-compatible Wayland compositors
License:        MIT
URL:            https://github.com/Mabi19/spaceshot
Source0:        spaceshot-0.6.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A batteries-included screenshot tool for wlroots-compatible Wayland compositors

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.2-1
- Initial openEuler RISC-V package from the full package inventory.
