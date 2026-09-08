# SPDX-License-Identifier: Apache-2.0
Name:           hyphen
Version:        2.8.9
Release:        1%{?dist}
Summary:        Hyphenation library and English hyphenation data
License:        GPL-2.0-or-later OR LGPL-2.1-or-later OR MPL-1.1
URL:            https://github.com/hunspell/hyphen
Source0:        hyphen-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
Hyphen provides a reusable hyphenation library, an English hyphenation
dictionary, and a helper for generating compact substring dictionaries.

%package devel
Summary:        Development files for Hyphen
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header and unversioned library link for developing applications with Hyphen.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libhyphen.la

%check
%make_build check

%files
%license COPYING COPYING.LGPL COPYING.MPL
%doc AUTHORS NEWS README README.compound README.hyphen README.nonstandard
%{_bindir}/substrings.pl
%{_datadir}/hyphen/
%{_libdir}/libhyphen.so.0*

%files devel
%license COPYING COPYING.LGPL COPYING.MPL
%{_includedir}/hyphen.h
%{_libdir}/libhyphen.so

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.8.9-1
- Initial openEuler RISC-V package.
