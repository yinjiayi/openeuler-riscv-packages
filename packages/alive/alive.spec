# SPDX-License-Identifier: Apache-2.0
Name:           alive
Version:        2.0.5
Release:        1%{?dist}
Summary:        Periodic ping program
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/alive/
Source0:        alive-2.0.5.tar.lz
BuildRequires:  gcc
BuildRequires:  lzip
BuildRequires:  make
BuildRequires:  guile-devel
BuildRequires:  iputils


%description
Periodic ping program

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.5-1
- Initial openEuler RISC-V package from the full package inventory.
