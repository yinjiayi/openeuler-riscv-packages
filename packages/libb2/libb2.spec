# SPDX-License-Identifier: Apache-2.0
Name:           libb2
Version:        0.98.1
Release:        1%{?dist}
Summary:        BLAKE2 hash-function library
License:        CC0-1.0
URL:            https://github.com/BLAKE2/libb2
Source0:        libb2-0.98.1.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make


%description
libb2 provides portable and optimized BLAKE2b, BLAKE2s, BLAKE2bp, and
BLAKE2sp hash functions.

%package devel
Summary:        Development files for libb2
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header and link metadata for developing applications with libb2.

%prep
%autosetup -p1
autoreconf -fi

%build
%configure --disable-static --disable-native
# Upstream configure replaces the distribution CFLAGS with -O3.  Restore the
# target flags so hardening and DWARF source mappings are retained.
%make_build CFLAGS="%{optflags} -fopenmp"

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
%make_build check CFLAGS="%{optflags} -fopenmp"

%files
%license COPYING
%doc README.md
%{_libdir}/libb2.so.1*

%files devel
%license COPYING
%{_includedir}/blake2.h
%{_libdir}/libb2.so
%{_libdir}/pkgconfig/libb2.pc

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.98.1-1
- Initial openEuler RISC-V package.
