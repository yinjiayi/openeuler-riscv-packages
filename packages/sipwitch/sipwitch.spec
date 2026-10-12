# SPDX-License-Identifier: Apache-2.0
Name:           sipwitch
Version:        1.9.15
Release:        1%{?dist}
Summary:        a federated SIP server, the GNU SIP Witch
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/sipwitch/
Source0:        sipwitch-1.9.15.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  gnutls-devel
BuildRequires:  ucommon-devel


%description
a federated SIP server, the GNU SIP Witch

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

%check
%make_build check

%files
%license COPYING
%doc AUTHORS
%doc ChangeLog
%doc NEWS
%doc README
%{_bindir}/*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.9.15-1
- Initial openEuler RISC-V package from the full package inventory.
