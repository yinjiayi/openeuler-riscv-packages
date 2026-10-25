# SPDX-License-Identifier: Apache-2.0
Name:           libdvbpsi
Version:        1.3.3
Release:        1%{?dist}
Summary:        Library for MPEG transport-stream and DVB PSI tables
License:        LGPL-2.1-or-later
URL:            https://www.videolan.org/developers/libdvbpsi.html
Source0:        libdvbpsi-%{version}.tar.bz2

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
libdvbpsi decodes and generates Program Specific Information tables in
MPEG transport streams and Digital Video Broadcasting data.

%package devel
Summary:        Development files for libdvbpsi
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
Public headers, unversioned linker name, and pkg-config metadata for
applications using libdvbpsi.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
# Upstream does not register its descriptor test with Automake's check
# target; run both that target and the complete in-tree descriptor test.
%make_build check
./misc/test_dr

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/libdvbpsi.so.10*

%files devel
%license COPYING
%{_includedir}/dvbpsi/
%{_libdir}/libdvbpsi.so
%{_libdir}/pkgconfig/libdvbpsi.pc

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.3-1
- Initial openEuler RISC-V package with upstream descriptor tests.
