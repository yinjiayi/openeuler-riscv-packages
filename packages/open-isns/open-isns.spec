# SPDX-License-Identifier: Apache-2.0
Name:           open-isns
Version:        0.101
Release:        1%{?dist}
Summary:        Partial Implementation of iSNS iSCSI registration
License:        LGPL-2.1-or-later
URL:            https://github.com/open-iscsi/open-isns
Source0:        open-isns-0.101.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Partial Implementation of iSNS iSCSI registration

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
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.101-1
- Initial openEuler RISC-V package from the full package inventory.
