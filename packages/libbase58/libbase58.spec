# SPDX-License-Identifier: Apache-2.0
Name:           libbase58
Version:        0.1.4
Release:        1%{?dist}
%global upstream_commit 16c2527608053d2cc2fa05b2e3b5ae96065d1410
Summary:        Base58 encoding and decoding library
License:        MIT
URL:            https://github.com/bitcoin/libbase58
Source0:        libbase58-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libgcrypt-devel
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  vim-common

%description
libbase58 is a small C library for encoding and decoding data using the
Bitcoin Base58 alphabet. It also ships a command-line encoder and decoder.

%package devel
Summary:        Development files for libbase58
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header, pkg-config metadata, and the unversioned linker name for developing
applications with libbase58.

%prep
%autosetup -n libbase58-%{upstream_commit} -p1

%build
./autogen.sh
%configure --enable-tool
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete
rm -f %{buildroot}%{_libdir}/libbase58.a
rm -f %{buildroot}%{_docdir}/%{name}/COPYING

%check
%make_build check

%files
%license COPYING
%doc AUTHORS README
%{_bindir}/base58
%{_libdir}/libbase58.so.0*

%files devel
%license COPYING
%{_includedir}/libbase58.h
%{_libdir}/libbase58.so
%{_libdir}/pkgconfig/libbase58.pc

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.4-1
- Initial openEuler RISC-V package with all 12 registered upstream tests.
