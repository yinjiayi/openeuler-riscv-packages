# SPDX-License-Identifier: Apache-2.0
Name:           c-graph
Version:        2.0.1
Release:        1%{?dist}
Summary:        Demonstrates the theory of convolution underlying engineering systems and signal analysis
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/c-graph/
Source0:        c-graph-2.0.1.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-gfortran
BuildRequires:  make
BuildRequires:  guile-devel


%description
Demonstrates the theory of convolution underlying engineering systems and signal analysis

%prep
%autosetup -p1

%build
%configure
# Upstream overwrites the distribution FCFLAGS; target PIE linking requires
# position-independent Fortran objects on RISC-V.
%make_build FCFLAGS="%{optflags} -fPIC"

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.1-1
- Initial openEuler RISC-V package from the full package inventory.
