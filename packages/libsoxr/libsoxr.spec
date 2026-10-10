# SPDX-License-Identifier: Apache-2.0
Name: libsoxr
Version: 0.1.3
Release: 1%{?dist}
Summary: High-quality sample-rate conversion library
License: LGPL-2.1-or-later
URL: https://sourceforge.net/p/soxr/wiki/Home/
Source0: soxr-%{version}-Source.tar.xz
BuildRequires: cmake
BuildRequires: gcc
BuildRequires: make
%description
The SoX Resampler library performs high-quality sample-rate conversion.
%package devel
Summary: Development files for libsoxr
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
Headers and metadata for libsoxr.
%prep
%autosetup -p1 -n soxr-%{version}-Source
%build
%cmake -S . -B "%{__cmake_builddir}" \
  -DBUILD_TESTS=ON \
  -DBUILD_EXAMPLES=ON \
  -DWITH_OPENMP=OFF
%cmake_build
%install
%cmake_install
%check
%ctest
%files
%license LICENCE
%doc README
%{_libdir}/libsoxr.so.0*
%{_libdir}/libsoxr-lsr.so.0*
%files devel
%{_includedir}/soxr.h
%{_includedir}/soxr-lsr.h
%{_libdir}/libsoxr.so
%{_libdir}/libsoxr-lsr.so
%{_libdir}/pkgconfig/soxr*.pc
%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.3-1
- Initial package.
