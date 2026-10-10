# SPDX-License-Identifier: Apache-2.0
Name:           mpdecimal
Version:        4.0.1
Release:        1%{?dist}
Summary:        Correctly rounded arbitrary-precision decimal arithmetic libraries
License:        BSD-2-Clause
URL:            https://www.bytereef.org/mpdecimal/
Source0:        mpdecimal-%{version}.tar.gz

BuildRequires:  curl
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconf
BuildRequires:  unzip

%description
mpdecimal supplies the C libmpdec and C++ libmpdec++ libraries for
correctly rounded arbitrary-precision decimal arithmetic.

%package devel
Summary:        Headers and pkg-config files for mpdecimal
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Development headers, linker names, and pkg-config metadata for libmpdec and
libmpdec++.

%prep
%autosetup -n mpdecimal-%{version} -p1

%build
CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" ./configure \
  --prefix=%{_prefix} --libdir=%{_libdir} --includedir=%{_includedir} \
  --mandir=%{_mandir} --enable-cxx --enable-static --enable-shared \
  --enable-doc --enable-pc
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libmpdec.a
rm -f %{buildroot}%{_libdir}/libmpdec++.a
rm -rf %{buildroot}%{_docdir}/mpdecimal

%check
# Upstream defaults to insecure HTTP for its copyrighted official vectors.
# Pre-fetch the exact official ZIP over HTTPS so gettests.sh does not download.
curl --fail --location --proto '=https' --tlsv1.2 --output dectest.zip \
  https://speleotrove.com/decimal/dectest.zip
echo 'b70a224cd52e82b7a8150aedac5efa2d0cb3941696fd829bdbe674f9f65c3926  dectest.zip' | sha256sum -c -
mkdir -p tests/testdata
unzip -q dectest.zip -d tests/testdata
test -f tests/testdata/add.decTest
%make_build check

%files
%license COPYRIGHT.txt
%doc README.txt CHANGELOG.txt
%{_libdir}/libmpdec.so.4*
%{_libdir}/libmpdec++.so.4*

%files devel
%license COPYRIGHT.txt
%{_includedir}/mpdecimal.h
%{_includedir}/decimal.hh
%{_libdir}/libmpdec.so
%{_libdir}/libmpdec++.so
%{_libdir}/pkgconfig/libmpdec.pc
%{_libdir}/pkgconfig/libmpdec++.pc
%{_mandir}/man3/mpdecimal.3*
%{_mandir}/man3/libmpdec.3*
%{_mandir}/man3/libmpdec++.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.0.1-1
- Initial openEuler RISC-V package with pinned official full test vectors.
