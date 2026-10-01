# SPDX-License-Identifier: Apache-2.0
Name:           libao
Version:        1.2.0
Release:        1%{?dist}
Summary:        Cross-platform audio output library
License:        GPL-2.0-or-later
URL:            https://www.xiph.org/ao/
Source0:        libao-%{version}.tar.gz
Patch0:         0001-pulse-declare-posix-headers.patch

BuildRequires:  alsa-lib-devel
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  pulseaudio-libs-devel

%description
Libao provides a common audio output API with built-in null and file drivers
and dynamically loaded audio-device plugins.

%package devel
Summary:        Development files for libao
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
Public headers, linker name, pkg-config metadata, and API documentation.

%prep
%autosetup -p1

%build
%configure --disable-static --enable-alsa --enable-pulse
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete
test -f %{buildroot}%{_libdir}/ao/plugins-4/libalsa.so
test -f %{buildroot}%{_libdir}/ao/plugins-4/libpulse.so

%check
%make_build -j1 check

%files
%license COPYING
%doc README AUTHORS CHANGES
%{_libdir}/libao.so.4*
%{_libdir}/ao/plugins-4/
%{_mandir}/man5/libao.conf.5*

%files devel
%license COPYING
%{_includedir}/ao/
%{_libdir}/libao.so
%{_libdir}/pkgconfig/ao.pc
%{_libdir}/ckport/db/libao.ckport
%{_datadir}/aclocal/ao.m4
%{_datadir}/doc/libao-%{version}/

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.0-1
- Package the official Xiph libao 1.2.0 release for openEuler RISC-V.
