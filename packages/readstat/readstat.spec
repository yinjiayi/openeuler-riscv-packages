# SPDX-License-Identifier: Apache-2.0
Name:           readstat
Version:        1.1.9
Release:        1%{?dist}
Summary:        Command-line tool (+ C library) for converting SAS, Stata, and SPSS files
License:        MIT
URL:            https://github.com/WizardMac/ReadStat
Source0:        readstat-1.1.9.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Command-line tool (+ C library) for converting SAS, Stata, and SPSS files

%prep
%autosetup -p1

%build
autoreconf -fi
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license LICENSE
%doc README.md
%doc NEWS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.9-1
- Initial openEuler RISC-V package from the full package inventory.
