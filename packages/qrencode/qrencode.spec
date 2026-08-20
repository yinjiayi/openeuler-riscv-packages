# SPDX-License-Identifier: Apache-2.0
%global upstream_commit 715e29fd4cd71b6e452ae0f4e36d917b43122ce8

Name:           qrencode
Version:        4.1.1
Release:        3%{?dist}
Summary:        QR Code encoding library and command-line tool
License:        LGPL-2.1-or-later
URL:            https://fukuchi.org/works/qrencode/
Source0:        libqrencode-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  libpng-devel
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf
BuildRequires:  SDL2-devel
Provides:       qrencode-libs = %{version}-%{release}

%description
libqrencode encodes data into QR Code symbols. This package contains the
shared library and the qrencode command-line image generator.

%package devel
Summary:        Development files for libqrencode
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Header, pkg-config metadata, and the unversioned linker name for developing
applications with libqrencode.

%package help
Summary:        Documentation for qrencode
BuildArch:      noarch

%description help
The qrencode manual page and upstream release documentation.

%prep
%autosetup -n libqrencode-%{upstream_commit} -p1

%build
autoreconf -fiv
%configure \
  --disable-static \
  --enable-thread-safety \
  --with-png \
  --with-tests \
  --with-tools
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libqrencode.la

%check
%make_build check

%files
%license COPYING
%{_bindir}/qrencode
%{_libdir}/libqrencode.so.4*

%files devel
%license COPYING
%{_includedir}/qrencode.h
%{_libdir}/libqrencode.so
%{_libdir}/pkgconfig/libqrencode.pc

%files help
%license COPYING
%doc ChangeLog NEWS README.md TODO
%{_mandir}/man1/qrencode.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.1.1-3
- Rebuild qrencode for openEuler RISC-V from Fedora 44 and frozen cross-distribution evidence.
