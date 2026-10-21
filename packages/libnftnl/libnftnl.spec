# SPDX-License-Identifier: Apache-2.0
Name:           libnftnl
Version:        1.3.1
Release:        1%{?dist}
Summary:        Userspace library for nftables netlink messages
License:        GPL-2.0-or-later
URL:            https://www.netfilter.org/projects/libnftnl/
Source0:        libnftnl-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  libmnl-devel
BuildRequires:  make
BuildRequires:  pkgconf

%description
libnftnl is a userspace library providing a low-level netlink programming
interface for the in-kernel nf_tables subsystem.

%package devel
Summary:        Development files for libnftnl
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and the unversioned shared-library link for
developing applications with libnftnl.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libnftnl.la

%check
# Run every maintained unit test shipped in the publisher release archive.
%make_build check

%files
%license COPYING
%{_libdir}/libnftnl.so.11*

%files devel
%license COPYING
%{_includedir}/libnftnl/
%{_libdir}/libnftnl.so
%{_libdir}/pkgconfig/libnftnl.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.1-1
- Update the openEuler RISC-V package to 1.3.1 with all upstream tests.
