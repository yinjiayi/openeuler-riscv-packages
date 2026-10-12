# SPDX-License-Identifier: Apache-2.0
Name:           ttype
Version:        1.0.0
Release:        1%{?dist}
Summary:        A terminal-based typing test application
License:        GPL-3.0-or-later
URL:            https://github.com/Srinath10X/ttype
Source0:        ttype-1.0.0.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A terminal-based typing test application

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
