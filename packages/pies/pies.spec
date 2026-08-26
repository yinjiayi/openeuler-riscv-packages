# SPDX-License-Identifier: Apache-2.0
Name:           pies
Version:        1.8
Release:        1%{?dist}
Summary:        Program Invocation and Execution Supervisor
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/pies/
Source0:        pies-1.8.tar.bz2
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  gettext-devel


%description
Program Invocation and Execution Supervisor

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8-1
- Initial openEuler RISC-V package from the full package inventory.
