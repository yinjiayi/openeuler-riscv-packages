# SPDX-License-Identifier: Apache-2.0
Name:           powertop
Version:        2.15
Release:        1%{?dist}
Summary:        A tool to diagnose issues with power consumption and power management
License:        GPL-2.0-or-later
URL:            https://github.com/fenrus75/powertop
Source0:        powertop-2.15.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
A tool to diagnose issues with power consumption and power management

%prep
%autosetup -p1

%build
autoreconf -fi
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
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.15-1
- Initial openEuler RISC-V package from the full package inventory.
