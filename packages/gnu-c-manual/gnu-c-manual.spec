# SPDX-License-Identifier: Apache-2.0
Name:           gnu-c-manual
Version:        0.2.5
Release:        1%{?dist}
Summary:        GNU C language reference manual
License:        GFDL-1.3-or-later
URL:            https://www.gnu.org/software/gnu-c-manual/
Source0:        gnu-c-manual-0.2.5.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  texinfo


%description
GNU C language reference manual

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
%license fdl.texi
%doc README
%{_bindir}/*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.5-1
- Initial openEuler RISC-V package from the full package inventory.
