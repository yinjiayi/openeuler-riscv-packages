# SPDX-License-Identifier: Apache-2.0

Name:           recode
Version:        3.7.15
Release:        1%{?dist}
Summary:        Character set conversion utility and library
License:        GPL-3.0-or-later AND LGPL-3.0-or-later AND BSD-2-Clause AND LicenseRef-OFSFDL
URL:            https://github.com/rrthomas/recode
Source0:        recode-%{version}.tar.gz

BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  help2man
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  python3
BuildRequires:  python3-Cython
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  texinfo

%description
Recode converts files between character sets and surfaces. This package
contains the command-line converter and the shared librecode library.

%package devel
Summary:        Development files for librecode
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       recode-static = %{version}-%{release}

%description devel
Public headers, static archive, and unversioned linker name for developing
applications with librecode.

%package help
Summary:        Documentation for recode
BuildArch:      noarch

%description help
The Recode Info manual, manual page, and upstream release documentation.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/librecode.la
rm -f %{buildroot}%{_infodir}/dir
%find_lang %{name}

%check
%make_build check

%files -f %{name}.lang
%license COPYING COPYING-LIB
%{_bindir}/recode
%{_libdir}/librecode.so.3*

%files devel
%license COPYING COPYING-LIB
%{_includedir}/recode.h
%{_includedir}/recodext.h
%{_libdir}/librecode.a
%{_libdir}/librecode.so

%files help
%license COPYING COPYING-LIB
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{_infodir}/recode.info*
%{_mandir}/man1/recode.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.7.15-1
- Rebuild Recode for openEuler RISC-V from Fedora 44 and frozen cross-distribution evidence.
