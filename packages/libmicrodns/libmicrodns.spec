# SPDX-License-Identifier: Apache-2.0

Name:           libmicrodns
Version:        0.2.0
Release:        1%{?dist}
Summary:        Minimal mDNS resolver and announcer library
License:        LGPL-2.1-or-later
URL:            https://github.com/videolabs/libmicrodns
Source0:        libmicrodns-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf-pkg-config

%description
libmicrodns is a small multicast DNS library for discovering and announcing
services over IPv4 and IPv6.

%package devel
Summary:        Development files for libmicrodns
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
Headers, the unversioned shared-library link, and pkg-config metadata for
developing applications with libmicrodns.

%prep
%autosetup -p1

%build
%meson -Dtests=enabled
%meson_build

%install
%meson_install

%check
%meson_test

%files
%license COPYING
%doc AUTHORS NEWS README.md
%{_libdir}/libmicrodns.so.1*

%files devel
%license COPYING
%{_includedir}/microdns/
%{_libdir}/libmicrodns.so
%{_libdir}/pkgconfig/microdns.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.0-1
- Initial openEuler RISC-V package with the complete maintained upstream test suite.
