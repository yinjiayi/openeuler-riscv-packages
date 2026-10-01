# SPDX-License-Identifier: Apache-2.0
Name:           berry
Version:        0.1.13
Release:        1%{?dist}
Summary:        A healthy, bite-sized window manager written over the XLib Library
License:        MIT
URL:            https://github.com/JLErvin/berry
Source0:        berry-0.1.13.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A healthy, bite-sized window manager written over the XLib Library

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
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.13-1
- Initial openEuler RISC-V package from the full package inventory.
