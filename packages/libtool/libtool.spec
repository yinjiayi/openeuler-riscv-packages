# SPDX-License-Identifier: Apache-2.0
Name:           libtool
Version:        2.6.2
Release:        1%{?dist}
Summary:        Generic library support scripts
License:        GPL-2.0-or-later AND GPL-2.0-or-later WITH Autoconf-exception-generic AND GPL-2.0-or-later WITH Libtool-exception AND LGPL-2.0-or-later WITH Libtool-exception AND GPL-3.0-or-later WITH Autoconf-exception-generic-3.0 AND MIT AND FSFAP AND FSFULLR AND FSFULLRWD AND GFDL-1.3-or-later AND X11
URL:            https://www.gnu.org/software/libtool/
Source0:        libtool-%{version}.tar.xz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  help2man
BuildRequires:  m4
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  texinfo

Requires:       autoconf
Requires:       automake
Requires:       findutils
Requires:       gcc
Requires:       sed
Requires:       tar

%description
GNU Libtool provides portable shell scripts and macros for building,
installing, and using shared and static libraries across Unix-like systems.

%package ltdl
Summary:        Runtime library for loading modules portably
License:        LGPL-2.0-or-later WITH Libtool-exception

%description ltdl
Libltdl is GNU Libtool's portable dynamic-module loading library.

%package ltdl-devel
Summary:        Development files for libltdl
License:        LGPL-2.0-or-later WITH Libtool-exception
Requires:       %{name}-ltdl%{?_isa} = %{version}-%{release}

%description ltdl-devel
Headers, unversioned linker name, and support sources for libltdl.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules
%make_build

%install
%make_install
rm -f %{buildroot}%{_infodir}/dir
rm -f %{buildroot}%{_libdir}/libltdl.a %{buildroot}%{_libdir}/libltdl.la

%check
%make_build check VERBOSE=yes

%files
%license COPYING
%doc AUTHORS ChangeLog* NEWS README THANKS TODO
%{_bindir}/libtool
%{_bindir}/libtoolize
%{_datadir}/aclocal/*.m4
%dir %{_datadir}/libtool
%{_datadir}/libtool/build-aux
%{_infodir}/libtool.info*
%{_mandir}/man1/libtool.1*
%{_mandir}/man1/libtoolize.1*

%files ltdl
%license libltdl/COPYING.LIB
%{_libdir}/libltdl.so.*

%files ltdl-devel
%license libltdl/COPYING.LIB
%doc libltdl/README
%{_includedir}/ltdl.h
%{_includedir}/libltdl/
%{_libdir}/libltdl.so
%{_datadir}/libtool
%exclude %{_datadir}/libtool/build-aux

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.6.2-1
- Initial openEuler RISC-V package from frozen cross-distribution and upstream evidence.
