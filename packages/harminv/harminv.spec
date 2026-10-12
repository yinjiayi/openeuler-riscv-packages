# SPDX-License-Identifier: Apache-2.0
Name:           harminv
Version:        1.4.2
Release:        1%{?dist}
Summary:        A free program to solve the problem of harmonic inversion
License:        GPL-2.0-or-later
URL:            https://github.com/NanoComp/harminv
Source0:        harminv-1.4.2.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A free program to solve the problem of harmonic inversion

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
%license COPYRIGHT
%doc README.md
%doc NEWS.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.2-1
- Initial openEuler RISC-V package from the full package inventory.
