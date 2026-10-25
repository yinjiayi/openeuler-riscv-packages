# SPDX-License-Identifier: Apache-2.0
Name:           libcdada
Version:        0.6.4
Release:        1%{?dist}
Summary:        C API for C++-backed basic data structures
License:        BSD-2-Clause
URL:            https://msune.github.io/libcdada/
Source0:        libcdada-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf
BuildRequires:  python3

%description
libcdada provides C interfaces for basic data structures implemented using
the C++ standard library.

%package devel
Summary:        Headers and code generator for libcdada
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python3

%description devel
Public headers, unversioned linker name, and cdada-gen custom-type code
generator for developing with libcdada.

%prep
%autosetup -n libcdada-81d9bcb5ec06fb33f5d5b093f0cd8fbfb06174b1 -p1

%build
autoreconf -fi
%configure --enable-shared --enable-static --with-tests --with-examples
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libcdada.a
rm -f %{buildroot}%{_libdir}/libcdada.la

%check
%make_build check

%files
%license LICENSE
%doc README.md CHANGELOG.md AUTHORS
%{_libdir}/libcdada.so.0*

%files devel
%license LICENSE
%{_includedir}/cdada.h
%{_includedir}/cdada/
%{_libdir}/libcdada.so
%{_bindir}/cdada-gen

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.4-1
- Initial openEuler RISC-V package with upstream Automake tests.
