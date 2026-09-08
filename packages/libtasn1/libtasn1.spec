# SPDX-License-Identifier: Apache-2.0
Name:           libtasn1
Version:        4.21.0
Release:        1%{?dist}
Summary:        ASN.1 library used by GnuTLS
License:        GPL-3.0-or-later AND LGPL-2.1-or-later AND GFDL-1.3-or-later
URL:            https://www.gnu.org/software/libtasn1/
Source0:        libtasn1-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
libtasn1 provides a C library and tools for Abstract Syntax Notation One
(ASN.1) structures using Distinguished Encoding Rules.

%package devel
Summary:        Development files for libtasn1
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, manuals, and the unversioned library link for
developing applications with libtasn1.

%prep
%autosetup -p1

%build
%configure --disable-static --enable-shared
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_infodir}/dir

%check
%make_build check

%files
%license COPYING COPYING.LESSERv2
%doc AUTHORS ChangeLog NEWS README.md THANKS
%{_bindir}/asn1Coding
%{_bindir}/asn1Decoding
%{_bindir}/asn1Parser
%{_libdir}/libtasn1.so.6*
%{_mandir}/man1/asn1*.1*

%files devel
%license COPYING COPYING.LESSERv2
%{_includedir}/libtasn1.h
%{_libdir}/libtasn1.so
%{_libdir}/pkgconfig/libtasn1.pc
%{_mandir}/man3/*.3*
%{_infodir}/libtasn1.info*

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.21.0-1
- Initial openEuler RISC-V package with upstream ASN.1 tests.
