# SPDX-License-Identifier: Apache-2.0
Name:           libxdo3
Version:        3.20211022.1
Release:        1%{?dist}
Summary:        Keyboard input simulation library (v3)
License:        BSD-3-Clause
URL:            https://github.com/jordansissel/xdotool
Source0:        libxdo3-3.20211022.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Keyboard input simulation library (v3)

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
%license COPYRIGHT
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.20211022.1-1
- Initial openEuler RISC-V package from the full package inventory.
