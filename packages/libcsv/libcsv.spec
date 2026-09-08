# SPDX-License-Identifier: Apache-2.0
Name:           libcsv
Version:        3.0.3
Release:        1%{?dist}
Summary:        Small streaming CSV parser and writer library
License:        LGPL-2.1-or-later
URL:            https://sourceforge.net/projects/libcsv/
Source0:        libcsv-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
libcsv is a small ANSI C library for parsing and writing comma-separated
value data through a streaming callback interface.

%package devel
Summary:        Development files for libcsv
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files, manual pages, and the unversioned shared library link for
developing applications with libcsv.

%prep
%autosetup -p1

%build
autoreconf -fi
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libcsv.la

%check
# Run the complete maintained parser and writer regression program.
%make_build check

%files
%license COPYING COPYING.LESSER
%doc ChangeLog FAQ README
%{_libdir}/libcsv.so.3*

%files devel
%license COPYING COPYING.LESSER
%{_includedir}/csv.h
%{_libdir}/libcsv.so
%{_mandir}/man3/csv.3*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.3-1
- Initial openEuler RISC-V package with the complete upstream regression gate.
