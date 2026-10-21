# SPDX-License-Identifier: Apache-2.0
Name:           libmpack
Version:        1.0.5
Release:        1%{?dist}
%global upstream_commit e9047afe4c02cd47c510f701deda6f502d7d94a2
Summary:        Small MessagePack and MessagePack-RPC C library
License:        MIT
URL:            https://github.com/libmpack/libmpack
Source0:        libmpack-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf

%description
libmpack is a small, allocation-free C library implementing MessagePack
serialization and MessagePack-RPC with incremental reader and writer APIs.

%package devel
Summary:        Development files for libmpack
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Amalgamated header, pkg-config metadata, and unversioned linker name for
developing applications with libmpack.

%prep
%autosetup -n libmpack-%{upstream_commit} -p1

%build
%make_build CFLAGS="%{optflags}" config=release MAJOR=1 MINOR=0 PATCH=5 \
  PREFIX=%{_prefix} LIBDIR=%{_libdir} INCDIR=%{_includedir} lib-bin test-bin

%install
%make_install config=release MAJOR=1 MINOR=0 PATCH=5 \
  PREFIX=%{_prefix} LIBDIR=%{_libdir} INCDIR=%{_includedir}
find %{buildroot} -name '*.la' -delete
rm -f %{buildroot}%{_libdir}/libmpack.a

%check
%make_build config=release MAJOR=1 MINOR=0 PATCH=5 \
  PREFIX=%{_prefix} LIBDIR=%{_libdir} INCDIR=%{_includedir} test

%files
%license LICENSE-MIT
%doc README.md
%{_libdir}/libmpack.so.0*

%files devel
%license LICENSE-MIT
%{_includedir}/mpack.h
%{_libdir}/libmpack.so
%{_libdir}/pkgconfig/mpack.pc

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.5-1
- Initial openEuler RISC-V package with the complete upstream TAP suite.
