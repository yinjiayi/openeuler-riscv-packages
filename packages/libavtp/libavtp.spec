# SPDX-License-Identifier: Apache-2.0
Name:           libavtp
Version:        0.2.0
Release:        1%{?dist}
Summary:        Audio Video Transport Protocol library
License:        BSD-3-Clause
URL:            https://github.com/Avnu/libavtp
Source0:        libavtp-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  libcmocka-devel
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf

%description
libavtp provides C helpers for constructing and parsing IEEE 1722 Audio Video
Transport Protocol data units.

%package devel
Summary:        Development files for libavtp
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, pkg-config metadata, and the unversioned linker name for developing
applications with libavtp.

%prep
%autosetup -p1

%build
%meson -Dtests=enabled
%meson_build

%install
%meson_install

%check
%meson_test

%files
%license LICENSE
%doc CONTRIBUTING.md HACKING.md README.md
%{_libdir}/libavtp.so.0*

%files devel
%license LICENSE
%{_includedir}/avtp.h
%{_includedir}/avtp_aaf.h
%{_includedir}/avtp_crf.h
%{_includedir}/avtp_cvf.h
%{_includedir}/avtp_ieciidc.h
%{_includedir}/avtp_rvf.h
%{_libdir}/libavtp.so
%{_libdir}/pkgconfig/avtp.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.0-1
- Initial openEuler RISC-V package with all seven upstream API test programs.
