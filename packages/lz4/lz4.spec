# SPDX-License-Identifier: Apache-2.0
Name:           lz4
Version:        1.10.0
Release:        1%{?dist}
Summary:        Fast lossless compression algorithm and tools
License:        BSD-2-Clause AND GPL-2.0-or-later
URL:            https://lz4.org/
Source0:        lz4-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
LZ4 is a lossless compression algorithm focused on high compression and
decompression speed. This package contains the shared library and CLI tools.

%package devel
Summary:        Development files for LZ4
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and the unversioned library link for developing
applications with LZ4.

%prep
%autosetup -p1

%build
%make_build lib-release lz4-release \
  CFLAGS="%{optflags}" \
  LDFLAGS="%{__global_ldflags}"

%install
%{__make} install \
  DESTDIR=%{buildroot} \
  PREFIX=%{_prefix} \
  LIBDIR=%{_libdir} \
  MANDIR=%{_mandir}
rm -f %{buildroot}%{_libdir}/liblz4.a

%check
%make_build check \
  CFLAGS="%{optflags}" \
  LDFLAGS="%{__global_ldflags}"

%files
%license LICENSE programs/COPYING
%doc NEWS README.md SECURITY.md
%{_bindir}/lz4
%{_bindir}/lz4c
%{_bindir}/lz4cat
%{_bindir}/unlz4
%{_libdir}/liblz4.so.1*
%{_mandir}/man1/lz4*.1*
%{_mandir}/man1/unlz4.1*

%files devel
%license LICENSE lib/LICENSE
%{_includedir}/lz4*.h
%{_libdir}/liblz4.so
%{_libdir}/pkgconfig/liblz4.pc

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.10.0-1
- Initial openEuler RISC-V package with upstream essential tests.
