# SPDX-License-Identifier: Apache-2.0
Name:           libHX
Version:        5.4
Release:        1%{?dist}
Summary:        Utility library for C and C++ programs
License:        GPL-3.0-only AND LGPL-2.1-or-later
URL:            https://inai.de/projects/libhx/
Source0:        libHX-%{version}.tar.zst

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  zstd

%description
libHX provides reusable C and C++ utilities including maps, deques, linked
lists, string formatting, option parsing, configuration parsing, casts,
filesystem helpers, and socket helpers.

%package devel
Summary:        Development files for libHX
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, C++ helper headers, pkg-config metadata, and the unversioned linker
name for developing applications with libHX.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f -- %{buildroot}%{_libdir}/libHX.la

%check
%{__make} check

%files
%license COPYING
%{_libdir}/libHX.so.43*

%files devel
%license COPYING
%{_includedir}/libHX.h
%{_includedir}/libHX/
%{_libdir}/libHX.so
%{_libdir}/pkgconfig/libHX.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.4-1
- Initial openEuler RISC-V package with every upstream check program enabled.
- Run the complete registered C and C++ test suite without downstream skips.
