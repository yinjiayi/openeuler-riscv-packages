# SPDX-License-Identifier: Apache-2.0
Name:           libatomic_ops
Version:        7.10.0
Release:        1%{?dist}
Summary:        Portable atomic memory operations library
License:        GPL-2.0-or-later AND MIT
URL:            https://github.com/ivmai/libatomic_ops
Source0:        libatomic_ops-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
libatomic_ops provides architecture-aware implementations of atomic memory
operations, including explicit RISC-V compiler backends.

%package devel
Summary:        Development files for libatomic_ops
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and unversioned library links for developing
applications with libatomic_ops and its GPL allocator and stack helpers.

%prep
%autosetup -p1

%build
%configure --disable-static --enable-shared
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_docdir}/libatomic_ops

%check
%make_build check

%files
%license LICENSE COPYING
%doc AUTHORS ChangeLog README.md README_details.txt README_malloc.txt README_stack.txt
%{_libdir}/libatomic_ops.so.1*
%{_libdir}/libatomic_ops_gpl.so.1*

%files devel
%license LICENSE COPYING
%{_includedir}/atomic_ops.h
%{_includedir}/atomic_ops_malloc.h
%{_includedir}/atomic_ops_stack.h
%{_includedir}/atomic_ops/
%{_libdir}/libatomic_ops.so
%{_libdir}/libatomic_ops_gpl.so
%{_libdir}/pkgconfig/atomic_ops.pc

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 7.10.0-1
- Initial openEuler RISC-V package with upstream atomic and thread tests.
