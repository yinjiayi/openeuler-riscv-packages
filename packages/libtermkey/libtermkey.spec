# SPDX-License-Identifier: Apache-2.0
Name:           libtermkey
Version:        0.22
Release:        1%{?dist}
%global upstream_commit c97f926ddcd1ade551162272bd4c8cf69e0b7de2
Summary:        Library for processing terminal keyboard input
License:        MIT
URL:            https://www.leonerd.org.uk/code/libtermkey/
Source0:        libtermkey-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  pkgconf
BuildRequires:  unibilium-devel

%description
libtermkey provides a simple C API for decoding keyboard input from terminal
applications, including Unicode, function keys, modifiers, mouse reports, and
terminal control replies.

%package devel
Summary:        Development files for libtermkey
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Header, pkg-config metadata, unversioned linker name, and API manual pages for
developing applications with libtermkey.

%prep
%autosetup -n libtermkey-%{upstream_commit} -p1

%build
%make_build \
  CFLAGS='%{build_cflags}' \
  LDFLAGS='%{build_ldflags}' \
  PREFIX=%{_prefix} \
  LIBDIR=%{_libdir}

%install
%make_install \
  PREFIX=%{_prefix} \
  LIBDIR=%{_libdir}
rm -f %{buildroot}%{_libdir}/libtermkey.la

%check
%make_build test \
  CFLAGS='%{build_cflags}' \
  LDFLAGS='%{build_ldflags}' \
  PREFIX=%{_prefix} \
  LIBDIR=%{_libdir}

%files
%license LICENSE
%{_libdir}/libtermkey.so.1*

%files devel
%license LICENSE
%{_includedir}/termkey.h
%{_libdir}/libtermkey.so
%{_libdir}/pkgconfig/termkey.pc
%{_mandir}/man3/termkey_*.3*
%{_mandir}/man7/termkey.7*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.22-1
- Initial openEuler RISC-V package with all maintained upstream TAP tests.
