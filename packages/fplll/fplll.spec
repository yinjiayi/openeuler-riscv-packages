# SPDX-License-Identifier: Apache-2.0
Name:           fplll
Version:        5.5.0
Release:        1%{?dist}
Summary:        Lattice algorithms using floating-point arithmetic
License:        LGPL-2.1-or-later
URL:            https://github.com/fplll/fplll
Source0:        fplll-5.5.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
Lattice algorithms using floating-point arithmetic

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
%doc NEWS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.5.0-1
- Initial openEuler RISC-V package from the full package inventory.
