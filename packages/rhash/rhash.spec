# SPDX-License-Identifier: Apache-2.0
Name:           rhash
Version:        1.4.6
Release:        1%{?dist}
Summary:        Utility and library for computing hash sums
License:        0BSD
URL:            https://github.com/rhash/RHash
Source0:        rhash-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
RHash is a command-line utility and C library for calculating and verifying
many hash sums, including SHA-2, SHA-3, BLAKE2, BLAKE3, Tiger, and TTH.

%package devel
Summary:        Development files for LibRHash
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, the unversioned shared-library link, and pkg-config metadata for
developing applications with LibRHash.

%prep
%autosetup -n RHash-%{version}

%build
INSTALL_INCDIR=%{_includedir} ./configure \
  --exec-prefix=%{_prefix} \
  --libdir=%{_libdir} \
  --mandir=%{_mandir} \
  --pkgconfigdir=%{_libdir}/pkgconfig \
  --sysconfdir=%{_sysconfdir}
%make_build OPTFLAGS="%{optflags}" OPTLDFLAGS="%{?__global_ldflags}" build

%install
%make_install
make DESTDIR=%{buildroot} install-lib-so-link install-lib-headers install-pkg-config

%check
make check
make test-full
make test-libs

%files
%license COPYING
%doc ChangeLog README.md
%config(noreplace) %{_sysconfdir}/rhashrc
%{_bindir}/*
%{_libdir}/librhash.so.1*
%{_mandir}/man1/*.1*

%files devel
%license COPYING
%{_includedir}/rhash.h
%{_includedir}/rhash_torrent.h
%{_libdir}/librhash.so
%{_libdir}/pkgconfig/librhash.pc

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.6-1
- Initial openEuler RISC-V package from Fedora 44 and cross-distribution evidence.
