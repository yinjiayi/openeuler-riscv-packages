# SPDX-License-Identifier: Apache-2.0
Name:           ppc64-diag
Version:        2.7.10
Release:        1%{?dist}
Summary:        PowerLinux Platform Diagnostics
License:        GPL-2.0-or-later
URL:            https://github.com/power-ras/ppc64-diag
Source0:        ppc64-diag-2.7.10.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
PowerLinux Platform Diagnostics

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
%license COPYING
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.7.10-1
- Initial openEuler RISC-V package from the full package inventory.
