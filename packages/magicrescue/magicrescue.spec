# SPDX-License-Identifier: Apache-2.0
Name:           magicrescue
Version:        1.1.10
Release:        1%{?dist}
Summary:        Find and recover deleted files on block devices
License:        GPL-2.0-or-later
URL:            https://github.com/jbj/magicrescue
Source0:        magicrescue-1.1.10.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Find and recover deleted files on block devices

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
%doc NEWS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.10-1
- Initial openEuler RISC-V package from the full package inventory.
