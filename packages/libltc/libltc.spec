# SPDX-License-Identifier: Apache-2.0
Name:           libltc
Version:        1.3.2
Release:        1%{?dist}
%global upstream_commit bf84b01097a1789c0296cc5fcfc3bf4608407930
Summary:        Linear timecode encoder and decoder library
License:        LGPL-3.0-or-later
URL:            https://x42.github.io/libltc/
Source0:        libltc-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf

%description
libltc provides a C library for encoding and decoding SMPTE linear timecode
audio signals, including frame alignment and timecode conversion helpers.

%package devel
Summary:        Development files for libltc
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Header, unversioned linker name, pkg-config metadata, and API documentation
for developing applications with libltc.

%prep
%autosetup -n libltc-%{upstream_commit} -p1

%build
autoreconf -fiv
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libltc.la

%check
%make_build check

%files
%license COPYING
%doc AUTHORS ChangeLog README.md
%{_libdir}/libltc.so.11*

%files devel
%license COPYING
%{_includedir}/ltc.h
%{_libdir}/libltc.so
%{_libdir}/pkgconfig/ltc.pc
%{_mandir}/man3/*.3*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.2-1
- Initial openEuler RISC-V package with the complete upstream test corpus.
