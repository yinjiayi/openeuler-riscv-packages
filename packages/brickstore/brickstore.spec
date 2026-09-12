# SPDX-License-Identifier: Apache-2.0
Name:           brickstore
Version:        2026.7.1
Release:        1%{?dist}
Summary:        Tool to manage LEGO inventory offline for BrickLink.
License:        GPL-3.0-or-later
URL:            https://github.com/rgriebl/brickstore
Source0:        brickstore-2026.7.1.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Tool to manage LEGO inventory offline for BrickLink.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license LICENSE.GPL
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2026.7.1-1
- Initial openEuler RISC-V package from the full package inventory.
