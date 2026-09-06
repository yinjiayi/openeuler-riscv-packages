# SPDX-License-Identifier: Apache-2.0
Name:           libsbsms
Version:        2.3.0
Release:        1%{?dist}
Summary:        A library for high quality time and pitch scale modification
License:        GPL-2.0-or-later
URL:            https://github.com/claytonotey/libsbsms
Source0:        libsbsms-2.3.0.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A library for high quality time and pitch scale modification

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
%license LICENSE.txt
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.0-1
- Initial openEuler RISC-V package from the full package inventory.
