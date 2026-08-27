# SPDX-License-Identifier: Apache-2.0
Name:           mairix
Version:        0.24
Release:        1%{?dist}
Summary:        A program for indexing and searching emails
License:        GPL-2.0-or-later
URL:            https://github.com/vandry/mairix
Source0:        mairix-0.24.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A program for indexing and searching emails

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

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.24-1
- Initial openEuler RISC-V package from the full package inventory.
