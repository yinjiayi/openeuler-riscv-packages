# SPDX-License-Identifier: Apache-2.0
Name:           dvbstreamer-t2
Version:        2.1.22
Release:        1%{?dist}
Summary:        Console-based application to stream DVB services over UDP (Stable DVB-T2 Release)
License:        GPL-2.0-or-later
URL:            https://github.com/ccdale/dvbstreamer
Source0:        dvbstreamer-t2-2.1.22.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Console-based application to stream DVB services over UDP (Stable DVB-T2 Release)

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
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.22-1
- Initial openEuler RISC-V package from the full package inventory.
