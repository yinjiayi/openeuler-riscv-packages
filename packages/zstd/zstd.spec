# SPDX-License-Identifier: Apache-2.0
Name:           zstd
Version:        1.5.7
Release:        1%{?dist}
Summary:        Fast real-time compression algorithm and tools
License:        BSD-3-Clause AND GPL-2.0-only
URL:            https://facebook.github.io/zstd/
Source0:        zstd-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
Zstandard is a lossless compression algorithm with a wide range of speed and
compression-ratio tradeoffs. This package contains the shared library and CLI.

%package devel
Summary:        Development files for Zstandard
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and the unversioned library link for developing
applications with Zstandard.

%prep
%autosetup -p1

%build
LDFLAGS="%{__global_ldflags}" \
%make_build lib-release zstd-release \
  CFLAGS="%{optflags}"

%install
%{__make} install \
  DESTDIR=%{buildroot} \
  PREFIX=%{_prefix} \
  LIBDIR=%{_libdir} \
  BINDIR=%{_bindir} \
  MANDIR=%{_mandir}
rm -f %{buildroot}%{_libdir}/libzstd.a

%check
LDFLAGS="%{__global_ldflags}" \
%make_build check \
  CFLAGS="%{optflags}"

%files
%license LICENSE COPYING
%doc CHANGELOG README.md SECURITY.md
%{_bindir}/unzstd
%{_bindir}/zstd
%{_bindir}/zstdcat
%{_bindir}/zstdgrep
%{_bindir}/zstdless
%{_bindir}/zstdmt
%{_libdir}/libzstd.so.1*
%{_mandir}/man1/unzstd.1*
%{_mandir}/man1/zstd*.1*

%files devel
%license LICENSE
%{_includedir}/zdict.h
%{_includedir}/zstd.h
%{_includedir}/zstd_errors.h
%{_libdir}/libzstd.so
%{_libdir}/pkgconfig/libzstd.pc

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.7-1
- Initial openEuler RISC-V package with upstream basic CLI tests.
