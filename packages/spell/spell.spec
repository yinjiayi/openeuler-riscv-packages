# SPDX-License-Identifier: Apache-2.0
Name:           spell
Version:        1.1
Release:        1%{?dist}
Summary:        A clone of the standard Unix program of the same name, implemented as a wrapper for Ispell
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/spell/
Source0:        spell-1.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  aspell
Requires:       aspell


%description
A clone of the standard Unix program of the same name, implemented as a wrapper for Ispell

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
%doc README
%{_bindir}/*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1-1
- Initial openEuler RISC-V package from the full package inventory.
