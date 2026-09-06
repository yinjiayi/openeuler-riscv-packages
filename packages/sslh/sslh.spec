# SPDX-License-Identifier: Apache-2.0
Name:           sslh
Version:        2.3.1
Release:        1%{?dist}
Summary:        SSL/SSH/OpenVPN/XMPP/tinc port multiplexer
License:        GPL-2.0-or-later
URL:            https://github.com/yrutschle/sslh
Source0:        sslh-2.3.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
SSL/SSH/OpenVPN/XMPP/tinc port multiplexer

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
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.1-1
- Initial openEuler RISC-V package from the full package inventory.
