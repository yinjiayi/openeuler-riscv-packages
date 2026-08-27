# SPDX-License-Identifier: Apache-2.0
Name:           clevo-indicator-dual
Version:        1.0.0
Release:        1%{?dist}
Summary:        Linux dual-fan control (CPU + GPU) for Clevo-based laptops and Axioo rebrands. Fork of clevo-indicator that drives BOTH fans instead of only the CPU fan.
License:        GPL-2.0-or-later
URL:            https://github.com/hajilok/clevo-axioo-dual-fan-linux
Source0:        clevo-indicator-dual-1.0.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Linux dual-fan control (CPU + GPU) for Clevo-based laptops and Axioo rebrands. Fork of clevo-indicator that drives BOTH fans instead of only the CPU fan.

%prep
%autosetup -p1

%build
%make_build

%install
%make_install PREFIX=%{_prefix}
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build test

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
