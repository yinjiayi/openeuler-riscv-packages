# SPDX-License-Identifier: Apache-2.0
Name:           libgfshare
Version:        2.0.0
Release:        1%{?dist}
%global upstream_commit da0566422af4e0ad5c9e17cfe21f563e4274338d
Summary:        Shamir secret-sharing library and tools
License:        MIT
URL:            https://github.com/kinnison/libgfshare
Source0:        libgfshare-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
libgfshare implements Shamir secret sharing over GF(2^8) and provides the
gfsplit and gfcombine command-line utilities.

%package devel
Summary:        Development files for libgfshare
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
Public C header, static archive, unversioned shared-library link, and
pkg-config metadata for developing against libgfshare.

%prep
%autosetup -n libgfshare-%{upstream_commit} -p1

%build
autoreconf --install --force
%configure
%make_build

%install
%make_install

%check
# Keep both C tests and the CLI split/combine roundtrip registered upstream.
%make_build check

%files
%license COPYRIGHT
%doc README AUTHORS
%{_bindir}/gfsplit
%{_bindir}/gfcombine
%{_libdir}/libgfshare.so.2*
%{_mandir}/man1/gfsplit.1*
%{_mandir}/man1/gfcombine.1*

%files devel
%license COPYRIGHT
%{_includedir}/libgfshare.h
%{_libdir}/libgfshare.so
%{_libdir}/libgfshare.a
%{_libdir}/libgfshare.la
%{_libdir}/pkgconfig/libgfshare.pc
%{_mandir}/man5/libgfshare.5*
%{_mandir}/man7/gfshare.7*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.0-1
- Package the official SHA-256-pinned upstream tag with all three tests.
