# SPDX-License-Identifier: Apache-2.0
Name:           boblight
Version:        2.1.0
Release:        1%{?dist}
Summary:        Collection of tools for driving lights connected to an external controller
License:        GPL-3.0-or-later
URL:            https://github.com/vdr-projects/boblight
Source0:        boblight-2.1.0.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Collection of tools for driving lights connected to an external controller

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
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
