# SPDX-License-Identifier: Apache-2.0
Name:           popt
Version:        1.19
Release:        1%{?dist}
Summary:        C library for parsing command-line parameters
License:        MIT
URL:            https://github.com/rpm-software-management/popt
Source0:        popt-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  libtool
BuildRequires:  make

%description
popt is a C library for parsing command-line options, including aliases and
automatic help generation.

%package devel
Summary:        Development files for popt
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header, pkg-config metadata, manual page, and unversioned library link for
developing applications with popt.

%prep
%autosetup -p1 -n popt-popt-%{version}-release

%build
autoreconf -fi
%configure --disable-static --enable-ld-version-script
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libpopt.la
%find_lang %{name}

%check
%make_build check

%files -f %{name}.lang
%license COPYING
%doc CREDITS README
%{_libdir}/libpopt.so.0*

%files devel
%license COPYING
%{_includedir}/popt.h
%{_libdir}/libpopt.so
%{_libdir}/pkgconfig/popt.pc
%{_mandir}/man3/popt.3*

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.19-1
- Initial openEuler RISC-V package.
