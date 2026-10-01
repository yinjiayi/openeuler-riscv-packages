# SPDX-License-Identifier: Apache-2.0
Name:           rsync-bpc
Version:        3.1.3.0
Release:        1%{?dist}
Summary:        A customized fork of rsync that is used as part of BackupPC
License:        GPL-3.0-or-later
URL:            https://github.com/backuppc/rsync-bpc
Source0:        rsync-bpc-3.1.3.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A customized fork of rsync that is used as part of BackupPC

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.1.3.0-1
- Initial openEuler RISC-V package from the full package inventory.
