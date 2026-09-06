# SPDX-License-Identifier: Apache-2.0
Name: lmdb
Version: 0.9.35
Release: 1%{?dist}
Summary: Lightning Memory-Mapped Database
License: OLDAP-2.8
URL: https://www.symas.com/lmdb
Source0: lmdb-%{version}.tar.gz
BuildRequires: gcc
BuildRequires: make
%description
LMDB is a fast transactional key-value database using memory-mapped files.
%package devel
Summary: Development files for LMDB
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
Headers and library links for LMDB.
%prep
%autosetup -p1 -n openldap-LMDB_%{version}
%build
%make_build -C libraries/liblmdb XCFLAGS="%{optflags}"
%install
%make_install -C libraries/liblmdb prefix=%{_prefix} libdir=%{_libdir}
%check
for t in mtest mtest2 mtest3 mtest4 mtest5; do ./libraries/liblmdb/$t; done
%files
%license libraries/liblmdb/LICENSE
%{_bindir}/mdb_copy
%{_bindir}/mdb_dump
%{_bindir}/mdb_load
%{_bindir}/mdb_stat
%{_libdir}/liblmdb.so
%files devel
%{_includedir}/lmdb.h
%{_libdir}/liblmdb.a
%{_mandir}/man1/mdb_*.1*
%{_mandir}/man3/mdb*.3*
%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.35-1
- Initial package.
