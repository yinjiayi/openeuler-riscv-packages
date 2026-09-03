# SPDX-License-Identifier: Apache-2.0
Name:           glpk
Version:        5.0
Release:        1%{?dist}
Summary:        GNU Linear Programming Kit: solve LP, MIP and other problems
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/glpk/
Source0:        glpk-5.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make


%description
GNU Linear Programming Kit: solve LP, MIP and other problems

%package devel
Summary:        Development files for GLPK
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header and unversioned shared-library link for developing applications with GLPK.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
%make_build check

%files
%license COPYING
%doc AUTHORS
%doc ChangeLog
%doc NEWS
%doc README
%{_bindir}/*
%{_libdir}/libglpk.so.40*

%files devel
%license COPYING
%{_includedir}/glpk.h
%{_libdir}/libglpk.so

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.0-1
- Initial openEuler RISC-V package from the full package inventory.
