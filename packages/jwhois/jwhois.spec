# SPDX-License-Identifier: Apache-2.0
Name:           jwhois
Version:        4.0
Release:        1%{?dist}
Summary:        An Internet Whois client
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/jwhois/
Source0:        jwhois-4.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make


%description
An Internet Whois client

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.0-1
- Initial openEuler RISC-V package from the full package inventory.
