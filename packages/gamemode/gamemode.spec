# SPDX-License-Identifier: Apache-2.0
Name:           gamemode
Version:        1.8.2
Release:        1%{?dist}
Summary:        A daemon/lib combo that allows games to request a set of optimisations be temporarily applied to the host OS
License:        BSD-3-Clause
URL:            https://github.com/FeralInteractive/gamemode
Source0:        gamemode-1.8.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A daemon/lib combo that allows games to request a set of optimisations be temporarily applied to the host OS

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
%license LICENSE.txt
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8.2-1
- Initial openEuler RISC-V package from the full package inventory.
