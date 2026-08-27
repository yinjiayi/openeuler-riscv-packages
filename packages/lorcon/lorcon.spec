# SPDX-License-Identifier: Apache-2.0
Name:           lorcon
Version:        2020.06.06
Release:        1%{?dist}
Summary:        Generic library for injecting 802.11 frames
License:        GPL-2.0-or-later
URL:            https://github.com/kismetwireless/lorcon
Source0:        lorcon-2020.06.06.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Generic library for injecting 802.11 frames

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
%license LICENSE
%doc README

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2020.06.06-1
- Initial openEuler RISC-V package from the full package inventory.
