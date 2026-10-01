# SPDX-License-Identifier: Apache-2.0
Name:           sirocco
Version:        2.1.1
Release:        2%{?dist}
Summary:        C++ library that allows to compute piecewise linear approximations of the path followed by the root of a complex polynomial
License:        GPL-3.0-or-later
URL:            https://github.com/miguelmarco/SIROCCO2
Source0:        sirocco-2.1.1.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gmp-devel
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  mpfr-devel

%description
C++ library that allows to compute piecewise linear approximations of the path followed by the root of a complex polynomial

%prep
%autosetup -n SIROCCO2-%{version} -p1

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

%changelog
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.1-2
- Match the case-sensitive source archive root.
- Add the GMP and MPFR development files required by the library and tests.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.1-1
- Initial openEuler RISC-V package from the full package inventory.
