# SPDX-License-Identifier: Apache-2.0
Name:           t2scan
Version:        0.7
Release:        1%{?dist}
Summary:        a small channel scan tool which generates DVB-T/T2 channels.conf files
License:        GPL-2.0-or-later
URL:            https://github.com/mighty-p/t2scan
Source0:        t2scan-0.7.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
a small channel scan tool which generates DVB-T/T2 channels.conf files

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license COPYING
%license LICENSE
%doc README
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7-1
- Initial openEuler RISC-V package from the full package inventory.
