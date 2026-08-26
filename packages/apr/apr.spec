# SPDX-License-Identifier: Apache-2.0
Name: apr
Version: 1.7.6
Release: 1%{?dist}
Summary: Apache Portable Runtime library
License: Apache-2.0
URL: https://apr.apache.org/
Source0: apr-%{version}.tar.bz2
BuildRequires: gcc
BuildRequires: make

%description
APR provides a predictable portable interface to operating-system services.

%package devel
Summary: Development files for APR
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, configuration tool, and build metadata for APR.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la

%check
%make_build test

%files
%license LICENSE NOTICE
%doc CHANGES README
%{_libdir}/libapr-1.so.0*

%files devel
%{_bindir}/apr-1-config
%{_includedir}/apr-1/
%{_libdir}/libapr-1.so
%{_libdir}/pkgconfig/apr-1.pc
%{_libdir}/apr.exp
%{_datadir}/apr-1/

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.7.6-1
- Initial openEuler RISC-V package from frozen lineage and official source evidence.
