# SPDX-License-Identifier: Apache-2.0
Name:           netcalc
Version:        2.1.7
Release:        1%{?dist}
Summary:        IP network calculator - Simplified clone of sipcalc with ipcalc looks
License:        BSD-3-Clause
URL:            https://github.com/troglobit/netcalc
Source0:        netcalc-2.1.7.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
IP network calculator - Simplified clone of sipcalc with ipcalc looks

%prep
%autosetup -p1

%build
autoreconf -fi
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license LICENSE
%doc README.md
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.7-1
- Initial openEuler RISC-V package from the full package inventory.
