# SPDX-License-Identifier: Apache-2.0
Name:           libpipeline
Version:        1.5.8
Release:        1%{?dist}
Summary:        C library for manipulating pipelines of subprocesses
License:        GPL-3.0-or-later
URL:            https://libpipeline.nongnu.org/
Source0:        libpipeline-%{version}.tar.gz

BuildRequires:  check-devel
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
libpipeline is a C library for constructing and running pipelines of
subprocesses without passing commands through a shell parser.

%package devel
Summary:        Development files for libpipeline
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, the unversioned library link, pkg-config metadata, and manual pages
for applications that use libpipeline.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libpipeline.la

%check
%make_build check

%files
%license COPYING
%doc ChangeLog NEWS.md README.md
%{_libdir}/libpipeline.so.1*

%files devel
%license COPYING
%{_includedir}/pipeline.h
%{_libdir}/libpipeline.so
%{_libdir}/pkgconfig/libpipeline.pc
%{_mandir}/man3/libpipeline.3*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.8-1
- Initial openEuler RISC-V package from reviewed Fedora 44 and upstream evidence.
