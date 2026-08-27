# SPDX-License-Identifier: Apache-2.0
Name:           nss-altfiles
Version:        2.23.0
Release:        1%{?dist}
Summary:        NSS module to look up users and other maps from /usr/lib
License:        LGPL-2.1-or-later
URL:            https://github.com/flatcar/nss-altfiles
Source0:        nss-altfiles-2.23.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
NSS module to look up users and other maps from /usr/lib

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.23.0-1
- Initial openEuler RISC-V package from the full package inventory.
