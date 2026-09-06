# SPDX-License-Identifier: Apache-2.0
Name:           yersinia
Version:        0.8.2
Release:        1%{?dist}
Summary:        A network tool designed to take advantage of some weakness in different network protocols
License:        GPL-2.0-or-later
URL:            https://github.com/tomac/yersinia
Source0:        yersinia-0.8.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A network tool designed to take advantage of some weakness in different network protocols

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
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.2-1
- Initial openEuler RISC-V package from the full package inventory.
