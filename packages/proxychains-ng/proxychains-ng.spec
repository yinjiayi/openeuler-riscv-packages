# SPDX-License-Identifier: Apache-2.0
Name:           proxychains-ng
Version:        4.17
Release:        1%{?dist}
Summary:        A hook preloader that allows to redirect TCP traffic of existing dynamically linked programs through one or more SOCKS or HTTP proxies
License:        GPL-2.0-or-later
URL:            https://github.com/rofl0r/proxychains-ng
Source0:        proxychains-ng-4.17.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A hook preloader that allows to redirect TCP traffic of existing dynamically linked programs through one or more SOCKS or HTTP proxies

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
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.17-1
- Initial openEuler RISC-V package from the full package inventory.
