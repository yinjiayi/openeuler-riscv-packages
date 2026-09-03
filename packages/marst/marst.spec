# SPDX-License-Identifier: Apache-2.0
Name:           marst
Version:        2.8
Release:        1%{?dist}
Summary:        Algol to C translator
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/marst/
Source0:        marst-2.8.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  gcc-c++


%description
Algol to C translator

%package devel
Summary:        Development files for the MARST Algol runtime
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header and unversioned shared-library link for programs using the MARST
Algol runtime library.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete

%check
%make_build check

%files
%license COPYING
%doc AUTHORS
%doc ChangeLog
%doc NEWS
%doc README
%{_bindir}/*
%{_libdir}/libalgol.so.0*

%files devel
%license COPYING
%{_includedir}/algol.h
%{_libdir}/libalgol.so

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.8-1
- Initial openEuler RISC-V package from the full package inventory.
