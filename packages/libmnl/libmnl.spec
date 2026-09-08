# SPDX-License-Identifier: Apache-2.0
Name:           libmnl
Version:        1.0.5
Release:        1%{?dist}
Summary:        Minimalistic Netlink userspace library
License:        LGPL-2.1-only
URL:            https://netfilter.org/projects/libmnl
Source0:        libmnl-%{version}.tar.bz2

BuildRequires:  gcc
BuildRequires:  make

%description
libmnl is a small userspace library for constructing and parsing Netlink
messages on Linux.

%package devel
Summary:        Development files for libmnl
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The public header, pkg-config metadata, and unversioned shared-library link
for developing applications with libmnl.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
%make_build check

%files
%license COPYING
%doc README
%{_libdir}/libmnl.so.0*

%files devel
%license COPYING
%{_includedir}/libmnl/
%{_libdir}/libmnl.so
%{_libdir}/pkgconfig/libmnl.pc

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.5-1
- Initial openEuler RISC-V package based on cross-distribution release evidence.
