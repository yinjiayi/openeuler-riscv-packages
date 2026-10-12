# SPDX-License-Identifier: Apache-2.0
Name:           intel-undervolt
Version:        1.7
Release:        1%{?dist}
Summary:        Intel CPU undervolting tool
License:        GPL-3.0-or-later
URL:            https://github.com/kitsunyan/intel-undervolt
Source0:        intel-undervolt-1.7.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Intel CPU undervolting tool

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
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.7-1
- Initial openEuler RISC-V package from the full package inventory.
