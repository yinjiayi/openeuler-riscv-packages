# SPDX-License-Identifier: Apache-2.0
Name:           libxcrypt
Version:        4.5.2
Release:        1%{?dist}
Summary:        Modern library for one-way password hashing
License:        LGPL-2.1-or-later AND BSD-3-Clause AND BSD-2-Clause AND BSD-2-Clause-FreeBSD AND 0BSD AND CC0-1.0 AND LicenseRef-Fedora-Public-Domain
URL:            https://github.com/besser82/libxcrypt
Source0:        libxcrypt-%{version}.tar.xz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  perl(:VERSION) >= 5.14
BuildRequires:  perl(Class::Struct)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(if)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(lib)
BuildRequires:  perl(open)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)
BuildRequires:  perl-interpreter

%description
Libxcrypt provides modern and historical password-hashing algorithms through
the traditional crypt, crypt_r, and extended crypt_gensalt interfaces.

%package devel
Summary:        Development files for libxcrypt
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Headers, manual pages, pkg-config metadata, and unversioned library links for
developing applications with libxcrypt.

%prep
%autosetup -p1

%build
%configure \
  --disable-static \
  --enable-hashes=all \
  --enable-obsolete-api=yes \
  --enable-obsolete-api-enosys=no \
  --enable-shared \
  --with-pkgconfigdir=%{_libdir}/pkgconfig
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete -print

%check
%make_build check

%files
%license AUTHORS COPYING.LIB LICENSING
%doc NEWS README THANKS TODO
%{_libdir}/libcrypt.so.1*
%{_libdir}/libowcrypt.so.1*
%{_mandir}/man5/crypt.5*

%files devel
%{_includedir}/crypt.h
%{_includedir}/xcrypt.h
%{_libdir}/libcrypt.so
%{_libdir}/libowcrypt.so
%{_libdir}/libxcrypt.so
%{_libdir}/pkgconfig/libcrypt.pc
%{_libdir}/pkgconfig/libxcrypt.pc
%{_mandir}/man3/crypt*.3*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.5.2-1
- Initial openEuler RISC-V package preserving the libcrypt.so.1 ABI.
