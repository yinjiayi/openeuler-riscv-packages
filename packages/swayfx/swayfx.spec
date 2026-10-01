# SPDX-License-Identifier: Apache-2.0
Name:           swayfx
Version:        0.5.3
Release:        1%{?dist}
Summary:        SwayFX: Sway, but with eye candy!
License:        MIT
URL:            https://github.com/WillPower3309/swayfx
Source0:        swayfx-0.5.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
SwayFX: Sway, but with eye candy!

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.5.3-1
- Initial openEuler RISC-V package from the full package inventory.
