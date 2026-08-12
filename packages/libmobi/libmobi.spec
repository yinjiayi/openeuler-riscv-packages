# SPDX-License-Identifier: Apache-2.0
Name:           libmobi
Version:        0.12
Release:        1%{?dist}
%global upstream_commit 85dcfe803fc2a21020ddcf15c3eb66b93d388add
Summary:        Library and tools for handling Mobipocket documents
License:        LGPL-3.0-or-later
URL:            https://github.com/bfabiszewski/libmobi
Source0:        libmobi-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  libxml2-devel
BuildRequires:  make
BuildRequires:  pkgconf
BuildRequires:  zlib-devel

%description
libmobi reads, writes, inspects, and extracts Mobipocket and Kindle document
containers. The package includes command-line metadata, extraction, and DRM
transformation tools.

%package devel
Summary:        Development files for libmobi
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Header, pkg-config metadata, and unversioned linker name for developing
applications with libmobi.

%prep
%autosetup -n libmobi-%{upstream_commit} -p1

%build
autoreconf -fi
%configure --with-libxml2 --with-zlib --enable-encryption
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
%make_build check

%files
%license COPYING
%doc AUTHORS ChangeLog README.md
%{_bindir}/mobidrm
%{_bindir}/mobimeta
%{_bindir}/mobitool
%{_libdir}/libmobi.so.0*
%{_mandir}/man1/mobidrm.1*
%{_mandir}/man1/mobimeta.1*
%{_mandir}/man1/mobitool.1*

%files devel
%license COPYING
%{_includedir}/mobi.h
%{_libdir}/libmobi.so
%{_libdir}/pkgconfig/libmobi.pc

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.12-1
- Initial openEuler RISC-V package with all 12 upstream sample tests.
