# SPDX-License-Identifier: Apache-2.0
Name:           libmpc
Version:        1.4.1
Release:        1%{?dist}
Summary:        Multiple-precision complex arithmetic library
License:        LGPL-3.0-or-later AND FSFAP
URL:            https://www.multiprecision.org/mpc/
Source0:        mpc-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  gmp-devel
BuildRequires:  make
BuildRequires:  mpfr-devel

%description
GNU MPC is a C library for arithmetic on complex numbers with arbitrarily
high precision and correctly rounded results.

%package devel
Summary:        Development files for GNU MPC
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gmp-devel%{?_isa}
Requires:       mpfr-devel%{?_isa}

%description devel
Header, pkg-config metadata, and unversioned linker name for GNU MPC.

%package help
Summary:        Documentation for GNU MPC
BuildArch:      noarch

%description help
GNU MPC reference documentation in Info format.

%prep
%autosetup -n mpc-%{version} -p1

%build
%configure --disable-silent-rules --disable-static --enable-shared
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_infodir}/dir

%check
%make_build check

%files
%license COPYING.LESSER
%doc AUTHORS NEWS README
%{_libdir}/libmpc.so.3*

%files devel
%license COPYING.LESSER
%{_includedir}/mpc.h
%{_libdir}/libmpc.so
%{_libdir}/pkgconfig/mpc.pc

%files help
%license COPYING.LESSER
%{_infodir}/mpc.info*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.1-1
- Initial openEuler RISC-V package from frozen cross-distribution and upstream evidence.
