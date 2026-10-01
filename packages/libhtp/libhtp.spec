# SPDX-License-Identifier: Apache-2.0
Name:           libhtp
Version:        0.5.53
Release:        1%{?dist}
Summary:        Security-aware HTTP protocol parser library
License:        BSD-3-Clause AND LicenseRef-Public-Domain
URL:            https://github.com/OISF/libhtp
Source0:        libhtp-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  zlib-devel

%description
LibHTP parses HTTP requests and responses for security-sensitive consumers.

%package devel
Summary:        Development files for libhtp
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       zlib-devel

%description devel
The public headers, pkg-config metadata, and library link for libhtp.

%prep
%autosetup -n libhtp-16e23594c61f7719f8cb1cd19ca69bbafb37a0eb

%build
./autogen.sh
%configure --disable-static --disable-silent-rules
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libhtp.la

%check
# The default upstream suite runs test_all over bundled HTTP fixtures and
# compiles test_fuzz, but does not start an unbounded fuzzing run.
%make_build check

%files
%license LICENSE
%doc README NOTICE docs/QUICK_START
%{_libdir}/libhtp.so.2*

%files devel
%license LICENSE
%{_includedir}/htp/
%{_libdir}/libhtp.so
%{_libdir}/pkgconfig/htp.pc

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.5.53-1
- Package official libhtp 0.5.53 with the complete registered upstream check suite.
