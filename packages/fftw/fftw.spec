# SPDX-License-Identifier: Apache-2.0
Name:           fftw
Version:        3.3.11
Release:        1%{?dist}
Summary:        Discrete Fourier transform library
License:        GPL-2.0-or-later
URL:            https://fftw.org/
Source0:        fftw-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
FFTW is a C library for computing discrete Fourier transforms. This build
provides the double-precision, POSIX-threaded, and OpenMP interfaces.

%package devel
Summary:        Development files for FFTW
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, Fortran interfaces, pkg-config and CMake metadata, manuals, and the
unversioned library links for developing applications with FFTW.

%prep
%autosetup -p1

%build
%configure \
  --disable-static \
  --enable-openmp \
  --enable-shared \
  --enable-threads
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_infodir}/dir

%check
%make_build check

%files
%license COPYING COPYRIGHT
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/fftw-wisdom
%{_bindir}/fftw-wisdom-to-conf
%{_libdir}/libfftw3.so.3*
%{_libdir}/libfftw3_omp.so.3*
%{_libdir}/libfftw3_threads.so.3*
%{_mandir}/man1/fftw*.1*

%files devel
%license COPYING COPYRIGHT
%{_includedir}/fftw3*
%{_libdir}/libfftw3.so
%{_libdir}/libfftw3_omp.so
%{_libdir}/libfftw3_threads.so
%{_libdir}/pkgconfig/fftw3.pc
%{_libdir}/cmake/fftw3/
%{_infodir}/fftw3.info*

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.3.11-1
- Initial openEuler RISC-V package with threaded upstream checks.
