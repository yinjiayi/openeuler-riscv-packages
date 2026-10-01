# SPDX-License-Identifier: Apache-2.0
Name:           libnfnetlink
Version:        1.0.2
Release:        1%{?dist}
Summary:        Low-level userspace library for Netfilter netlink messages
License:        GPL-2.0-only
URL:            https://netfilter.org/projects/libnfnetlink/
Source0:        libnfnetlink-%{version}.tar.bz2

BuildRequires:  gcc
BuildRequires:  make

%description
libnfnetlink provides low-level userspace helpers for constructing and
handling messages carried by the Linux Netfilter netlink transport.

%package devel
Summary:        Development files for libnfnetlink
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and the unversioned shared-library link for
developing Netfilter userspace applications with libnfnetlink.

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
%{_libdir}/libnfnetlink.so.0*

%files devel
%license COPYING
%{_includedir}/libnfnetlink/
%{_libdir}/libnfnetlink.so
%{_libdir}/pkgconfig/libnfnetlink.pc

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.2-1
- Initial openEuler RISC-V package from the full package inventory.
