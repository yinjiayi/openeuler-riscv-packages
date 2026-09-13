# SPDX-License-Identifier: Apache-2.0
Name:           libntlm
Version:        1.8
Release:        1%{?dist}
Summary:        NTLM authentication protocol client library
License:        LGPL-2.1-or-later AND GPL-3.0-or-later
URL:            https://savannah.nongnu.org/projects/libntlm/
Source0:        libntlm-1.8.tar.gz

BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf

%description
Libntlm is a small client-side implementation of the NTLM authentication
protocol. It provides helpers for constructing and parsing NTLM messages.

%package devel
Summary:        Development files for libntlm
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, the unversioned linker symlink, and pkg-config metadata for programs
using libntlm.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libntlm.la

%check
%make_build check

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README THANKS
%{_libdir}/libntlm.so.0*

%files devel
%license COPYING
%{_includedir}/ntlm.h
%{_libdir}/libntlm.so
%{_libdir}/pkgconfig/libntlm.pc

%changelog
* Fri Aug 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8-1
- Initial package from the official libntlm 1.8 release archive.
- Keep the complete upstream authentication and CVE regression tests enabled.
