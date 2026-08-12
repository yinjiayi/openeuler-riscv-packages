# SPDX-License-Identifier: Apache-2.0
Name:           libmodbus
Version:        3.2.0
Release:        1%{?dist}
%global upstream_commit a9b025d12289855490b10d77461c99e001abfc0f
Summary:        Fast and portable Modbus protocol library
License:        LGPL-2.1-or-later
URL:            https://libmodbus.org/
Source0:        libmodbus-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf
BuildRequires:  psmisc

%description
libmodbus is a C library providing Modbus RTU and TCP client and server APIs.
It is designed for portable applications on Linux and other operating systems.

%package devel
Summary:        Development files for libmodbus
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, pkg-config metadata, and unversioned linker name for developing
applications with libmodbus.

%prep
%autosetup -n libmodbus-%{upstream_commit} -p1

%build
autoreconf -fi
%configure --enable-tests --disable-static
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
%make_build check || {
  for log in tests/unit-test-server.log tests/unit-test-client.log; do
    test ! -f "$log" || { echo "=== $log ==="; cat "$log"; }
  done
  exit 1
}
(cd tests && ./proxy-tests.sh)

%files
%license COPYING.LESSER
%doc AUTHORS NEWS.md README.md
%{_libdir}/libmodbus.so.5*

%files devel
%license COPYING.LESSER
%{_includedir}/modbus/
%{_libdir}/libmodbus.so
%{_libdir}/pkgconfig/libmodbus.pc

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2.0-1
- Initial openEuler RISC-V package with unit and proxy integration tests.
