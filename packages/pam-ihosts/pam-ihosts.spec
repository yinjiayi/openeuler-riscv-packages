# SPDX-License-Identifier: Apache-2.0
Name:           pam-ihosts
Version:        1.6
Release:        1%{?dist}
Summary:        A PAM module that provides access control by ip, mac-address, or country-code/region
License:        GPL-3.0-or-later
URL:            https://github.com/ColumPaget/pam_ihosts
Source0:        pam-ihosts-1.6.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A PAM module that provides access control by ip, mac-address, or country-code/region

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
%license LICENCE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6-1
- Initial openEuler RISC-V package from the full package inventory.
