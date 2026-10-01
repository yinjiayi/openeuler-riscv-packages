# SPDX-License-Identifier: Apache-2.0
Name:           autogrid4
Version:        4.2.9
Release:        1%{?dist}
Summary:        Autogrid4 is a support software for docking programs such as AutoDock4 and Autodock-GPU. Its function is to precalculate the grids used by the docking softw
License:        GPL-2.0-or-later
URL:            https://github.com/ccsb-scripps/AutoGrid
Source0:        autogrid4-4.2.9.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Autogrid4 is a support software for docking programs such as AutoDock4 and Autodock-GPU. Its function is to precalculate the grids used by the docking softw

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
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.2.9-1
- Initial openEuler RISC-V package from the full package inventory.
