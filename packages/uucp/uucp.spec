# SPDX-License-Identifier: Apache-2.0
Name:           uucp
Version:        1.07
Release:        1%{?dist}
Summary:        Taylor UUCP is a free implementation of UUCP and is the standard UUCP used on the GNU system
License:        GPL-2.0-or-later
URL:            https://www.gnu.org/software/uucp/
Source0:        uucp-1.07.tar.gz
BuildRequires:  gcc
BuildRequires:  make


%description
Taylor UUCP is a free implementation of UUCP and is the standard UUCP used on the GNU system

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.07-1
- Initial openEuler RISC-V package from the full package inventory.
