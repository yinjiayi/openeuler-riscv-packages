# SPDX-License-Identifier: Apache-2.0
Name:           dtach-ng
Version:        0.10.1
Release:        1%{?dist}
Summary:        emulates the detach feature of screen
License:        GPL-2.0-or-later
URL:            https://github.com/xPMo/dtach
Source0:        dtach-ng-0.10.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
emulates the detach feature of screen

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
%license COPYING
%doc README

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.10.1-1
- Initial openEuler RISC-V package from the full package inventory.
