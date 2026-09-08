# SPDX-License-Identifier: Apache-2.0
Name:           libexif
Version:        0.6.26
Release:        1%{?dist}
Summary:        Library for parsing EXIF metadata
License:        LGPL-2.1-or-later
URL:            https://github.com/libexif/libexif
Source0:        libexif-0.6.26.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  libtool
BuildRequires:  make


%description
libexif parses Exchangeable Image File Format metadata from image files.

%package devel
Summary:        Development files for libexif
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and pkg-config metadata for developing applications with libexif.

%prep
%autosetup -p1
autoreconf -fi

%build
%configure --disable-static
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete
rm -rf -- %{buildroot}%{_docdir}/libexif
%find_lang libexif-12

%check
%make_build check

%files -f libexif-12.lang
%license COPYING
%doc AUTHORS ChangeLog NEWS README SECURITY.md
%{_libdir}/libexif.so.12*

%files devel
%license COPYING
%{_includedir}/libexif/
%{_libdir}/libexif.so
%{_libdir}/pkgconfig/libexif.pc

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.26-1
- Initial openEuler RISC-V package.
