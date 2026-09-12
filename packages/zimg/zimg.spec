# SPDX-License-Identifier: Apache-2.0
Name:           zimg
Version:        3.0.6
Release:        1%{?dist}
Summary:        Scaling, colorspace, and depth conversion library
License:        WTFPL
URL:            https://github.com/sekrit-twc/zimg
Source0:        zimg-release-%{version}.tar.gz
Source1:        googletest-703bd9caab50b139428cea1aaff9974ebee5742e.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  cmake
BuildRequires:  coreutils
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  tar

%description
zimg implements high-quality image scaling, colorspace conversion, and pixel
depth conversion through a small C and C++ API.

%package devel
Summary:        Development files for zimg
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Public C/C++ headers, linker name, and pkg-config metadata for zimg.

%prep
%autosetup -p1 -n zimg-release-%{version}
mkdir -p test/extra/googletest
tar -xzf %{SOURCE1} --strip-components=1 -C test/extra/googletest

%build
./autogen.sh
%configure --disable-static --enable-shared --enable-unit-test
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_docdir}/zimg

%check
%make_build check

%files
%license COPYING
%doc ChangeLog README.md
%{_libdir}/libzimg.so.*

%files devel
%{_includedir}/zimg.h
%{_includedir}/zimg++.hpp
%{_libdir}/libzimg.so
%{_libdir}/pkgconfig/zimg.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.6-1
- Initial openEuler RISC-V package with the complete offline unit-test suite.
