# SPDX-License-Identifier: Apache-2.0
Name:           hp2xx
Version:        3.4.4
Release:        1%{?dist}
Summary:        Converts HP-GL Plotter Language into a Variety of Formats
License:        GPL-2.0-or-later
URL:            https://www.gnu.org/software/hp2xx/
Source0:        hp2xx-3.4.4.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel


%description
Converts HP-GL Plotter Language into a Variety of Formats

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
%license copying
%doc AUTHORS
%doc CHANGES
%doc README
%{_bindir}/*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.4.4-1
- Initial openEuler RISC-V package from the full package inventory.
