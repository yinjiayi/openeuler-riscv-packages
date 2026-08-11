# SPDX-License-Identifier: Apache-2.0
Name:           libidn2
Version:        2.3.8
Release:        1%{?dist}
Summary:        IDNA2008, Punycode, and TR46 implementation
License:        (GPL-2.0-or-later OR LGPL-3.0-or-later) AND GPL-3.0-or-later
URL:            https://www.gnu.org/software/libidn/#libidn2
Source0:        libidn2-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  libunistring-devel
BuildRequires:  make
BuildRequires:  texinfo

%description
Libidn2 implements IDNA2008, Punycode, and Unicode TR46 for internationalized
domain names.

%package devel
Summary:        Development files for libidn2
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Headers, pkg-config metadata, API documentation, examples, manual pages, and
the unversioned library link for developing applications with libidn2.

%package -n idn2
Summary:        Command-line IDNA2008 and Punycode utility
License:        GPL-3.0-or-later
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n idn2
The idn2 command converts internationalized domain names to and from their
ASCII-compatible Punycode representation.

%prep
%autosetup -p1

%build
%configure --disable-rpath --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_infodir}/dir
%find_lang %{name}

%check
%make_build check

%files -f %{name}.lang
%license COPYING COPYING.LESSERv3 COPYING.unicode COPYINGv2
%doc AUTHORS NEWS README.md
%{_libdir}/libidn2.so.0*

%files devel
%license COPYING COPYING.LESSERv3 COPYING.unicode COPYINGv2
%doc examples/
%{_includedir}/idn2.h
%{_libdir}/libidn2.so
%{_libdir}/pkgconfig/libidn2.pc
%{_mandir}/man3/idn2_*.3*
%{_datadir}/gtk-doc/

%files -n idn2
%license COPYING
%{_bindir}/idn2
%{_infodir}/libidn2.info*
%{_mandir}/man1/idn2.1*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.8-1
- Initial openEuler RISC-V package with the complete upstream test suite.
