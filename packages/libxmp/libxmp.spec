# SPDX-License-Identifier: Apache-2.0
%global abi 4

Name:           libxmp
Version:        4.7.2
Release:        1%{?dist}
Summary:        Multi-format module playback library
License:        0BSD AND BSD-3-Clause AND ISC AND MIT AND LicenseRef-Fedora-Public-Domain
URL:            https://xmp.sourceforge.net/
Source0:        libxmp-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
libxmp renders tracker module files to PCM audio. It supports mainstream and
historical formats including MOD, S3M, XM, and IT, together with several
compressed module containers.

%package devel
Summary:        Development files for libxmp
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header, unversioned shared-library link, pkg-config metadata, CMake metadata,
and manual page for developing applications with libxmp.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
install -Dpm0644 docs/libxmp.3 %{buildroot}%{_mandir}/man3/libxmp.3

%check
%make_build check

%files
%license docs/COPYING
%doc README docs/Changelog docs/CREDITS
%{_libdir}/libxmp.so.%{abi}{,.*}

%files devel
%doc docs/libxmp.html docs/libxmp.pdf docs/fixloop.txt docs/formats.txt
%{_includedir}/xmp.h
%{_libdir}/libxmp.so
%dir %{_libdir}/cmake/libxmp
%{_libdir}/cmake/libxmp/libxmp-config.cmake
%{_libdir}/cmake/libxmp/libxmp-config-version.cmake
%{_libdir}/pkgconfig/libxmp.pc
%{_mandir}/man3/libxmp.3*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.7.2-1
- Initial openEuler RISC-V package from Fedora 44 and frozen cross-distribution evidence.
