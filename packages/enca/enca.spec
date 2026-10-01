# SPDX-License-Identifier: Apache-2.0
Name:           enca
Version:        1.22
Release:        1%{?dist}
Summary:        Charset analyzer and converter
License:        GPL-2.0-only AND LicenseRef-Public-Domain
URL:            https://cihar.com/software/enca/
Source0:        enca-%{version}.tar.xz
Patch0:         0001-tests-select-librecode-converter.patch

BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  recode
BuildRequires:  recode-devel
Requires:       recode

%description
Enca detects the character set and encoding of text and can convert text
through built-in iconv, librecode, and external converter interfaces.

%package devel
Summary:        Development files for libenca
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Public-domain header, pkg-config metadata, and the unversioned shared-library
link for developing applications with libenca.

%prep
%autosetup -p1

%build
%configure \
  --disable-static \
  --enable-external \
  --with-librecode
%make_build
chmod 0755 script/recode

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
%make_build check

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README.md THANKS
%{_bindir}/enca
%{_bindir}/enconv
%{_libdir}/libenca.so.0*
%{_libexecdir}/enca/
%{_mandir}/man1/enca.1*
%{_mandir}/man1/enconv.1*

%files devel
%license COPYING
%{_includedir}/enca.h
%{_libdir}/libenca.so
%{_libdir}/pkgconfig/enca.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.22-1
- Update Enca for openEuler RISC-V with complete librecode-enabled upstream tests.
- Select the external GNU recode wrapper by its complete build-tree path in the TeX regression test.
