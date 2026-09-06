# SPDX-License-Identifier: Apache-2.0
Name:           wavpack
Version:        5.9.0
Release:        1%{?dist}
Summary:        Hybrid lossless audio compression tools and library
License:        BSD-3-Clause AND LicenseRef-Public-Domain
URL:            https://www.wavpack.com/
Source0:        wavpack-%{version}.tar.xz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
WavPack is a lossless audio compression format and implementation. This
package provides the command-line encoder, decoder, gain scanner, tag editor,
and the versioned shared library.

%package devel
Summary:        Development files for WavPack
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header, unversioned shared-library link, pkg-config metadata, and CMake
metadata for developing applications with WavPack.

%prep
%autosetup -p1 -n wavpack-%{version}

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_TESTING=ON \
  -DWAVPACK_BUILD_PROGRAMS=ON \
  -DWAVPACK_ENABLE_DSD=ON \
  -DWAVPACK_ENABLE_LEGACY=ON \
  -DWAVPACK_ENABLE_THREADS=ON
%cmake_build

%install
%cmake_install

%check
# CTest runs upstream's short, no-extras exhaustive gate; the second command
# retains the complete all-tests workload at the supported twelve-thread max.
%ctest --output-on-failure --parallel 1
"%{_vpath_builddir}/wvtest" --threads=12 --exhaustive

%files
%license COPYING cli/md5.h
%doc AUTHORS ChangeLog NEWS README.md
%{_bindir}/wavpack
%{_bindir}/wvgain
%{_bindir}/wvtag
%{_bindir}/wvunpack
%{_libdir}/libwavpack.so.1*
%{_mandir}/man1/wavpack.1*
%{_mandir}/man1/wvgain.1*
%{_mandir}/man1/wvtag.1*
%{_mandir}/man1/wvunpack.1*

%files devel
%license COPYING cli/md5.h
%{_includedir}/wavpack/
%{_libdir}/cmake/WavPack/
%{_libdir}/libwavpack.so
%{_libdir}/pkgconfig/wavpack.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.9.0-1
- Initial openEuler RISC-V package from Fedora 44 and cross-distribution evidence.
