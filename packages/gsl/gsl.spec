# SPDX-License-Identifier: Apache-2.0
Name:           gsl
Version:        2.8
Release:        1%{?dist}
Summary:        GNU Scientific Library for numerical analysis
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/gsl/
Source0:        gsl-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf

%description
The GNU Scientific Library provides a broad collection of numerical-analysis
routines for vectors, matrices, special functions, transforms, statistics,
optimization, integration, differential equations, and random distributions.

%package devel
Summary:        Development files for GSL
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, configuration helpers, pkg-config metadata, and unversioned linker
names for GSL and its CBLAS implementation.

%package help
Summary:        Documentation for GSL
BuildArch:      noarch

%description help
The GNU Scientific Library reference manual and upstream release
documentation.

%prep
%autosetup -p1

%build
export CFLAGS="%{optflags} -ffp-contract=off"
%configure \
  --disable-silent-rules \
  --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_infodir}/dir
rm -f %{buildroot}%{_libdir}/*.la

%check
%make_build check

%files
%license COPYING
%{_bindir}/gsl-histogram
%{_bindir}/gsl-randist
%{_libdir}/libgsl.so.28*
%{_libdir}/libgslcblas.so.0*
%{_mandir}/man1/gsl-histogram.1*
%{_mandir}/man1/gsl-randist.1*

%files devel
%license COPYING
%{_bindir}/gsl-config
%{_includedir}/gsl/
%{_libdir}/libgsl.so
%{_libdir}/libgslcblas.so
%{_libdir}/pkgconfig/gsl.pc
%{_datadir}/aclocal/gsl.m4
%{_mandir}/man1/gsl-config.1*
%{_mandir}/man3/gsl.3*

%files help
%license COPYING
%doc AUTHORS BUGS ChangeLog NEWS README THANKS TODO
%{_infodir}/gsl-ref.info*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.8-1
- Initial openEuler RISC-V package from frozen cross-distribution and upstream evidence.
