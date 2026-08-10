# SPDX-License-Identifier: Apache-2.0
Name:           libdmtx
Version:        0.7.8
Release:        1%{?dist}
Summary:        Data Matrix barcode encoding and decoding library
License:        BSD-2-Clause
URL:            https://github.com/dmtx/libdmtx
Source0:        libdmtx-0.7.8.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make


%description
libdmtx reads and writes Data Matrix two-dimensional barcodes.

%package devel
Summary:        Development files for libdmtx
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header and link library for developing applications with libdmtx.

%prep
%autosetup -p1
autoreconf -fi

%build
%configure --disable-static
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
%make_build check

%files
%license LICENSE
%doc README
%{_libdir}/libdmtx.so.0*

%files devel
%license LICENSE
%{_includedir}/dmtx.h
%{_libdir}/libdmtx.so
%{_libdir}/pkgconfig/libdmtx.pc

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7.8-1
- Initial openEuler RISC-V package.
