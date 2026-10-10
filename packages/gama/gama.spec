# SPDX-License-Identifier: Apache-2.0
Name:           gama
Version:        2.33
Release:        1%{?dist}
Summary:        Package dedicated to the adjustment of surveying networks
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/gama/
Source0:        gama-2.33.tar.gz
BuildRequires:  expat-devel
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  gcc-c++


%description
Package dedicated to the adjustment of surveying networks

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
%doc README.md
%{_bindir}/*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.33-1
- Initial openEuler RISC-V package from the full package inventory.
