# SPDX-License-Identifier: Apache-2.0
Name:           hopm
Version:        1.1.10
Release:        1%{?dist}
Summary:        Hybrid Open Proxy Monitor - an open proxy scanner designed for IRC networks
License:        GPL-2.0-or-later
URL:            https://github.com/ircd-hybrid/hopm
Source0:        hopm-1.1.10.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Hybrid Open Proxy Monitor - an open proxy scanner designed for IRC networks

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
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.10-1
- Initial openEuler RISC-V package from the full package inventory.
