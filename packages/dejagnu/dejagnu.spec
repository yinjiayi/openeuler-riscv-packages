# SPDX-License-Identifier: Apache-2.0
Name:           dejagnu
Version:        1.6.3
Release:        1%{?dist}
Summary:        Framework for testing other programs
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/dejagnu/
Source0:        dejagnu-1.6.3.tar.gz
BuildArch:      noarch
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  expect
BuildRequires:  tcl


%description
Framework for testing other programs

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.3-1
- Initial openEuler RISC-V package from the full package inventory.
