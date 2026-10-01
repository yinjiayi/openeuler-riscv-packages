# SPDX-License-Identifier: Apache-2.0
Name:           libunwind
Version:        1.8.3
Release:        1%{?dist}
Summary:        Portable and efficient call-chain library
License:        MIT
URL:            https://www.nongnu.org/libunwind/
Source0:        libunwind-1.8.3.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  xz-devel
BuildRequires:  zlib-devel

%description
libunwind provides a portable C ABI for determining the call-chain of a
program and supports local and remote stack unwinding.

%package devel
Summary:        Development files for libunwind
Requires:       libunwind%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and shared-library links for libunwind.

%prep
%autosetup -p1

%build
%configure --disable-static --enable-shared --disable-documentation \
  --enable-setjmp=no
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
%make_build check

%ldconfig_scriptlets

%files
%license COPYING
%doc README NEWS
%{_libdir}/libunwind*.so.*

%files devel
%{_includedir}/unwind.h
%{_includedir}/libunwind*.h
%{_libdir}/libunwind*.so
%{_libdir}/pkgconfig/libunwind*.pc

%changelog
* Sun Aug 16 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8.3-1
- Package libunwind shared libraries and the complete upstream test suite.
