# SPDX-License-Identifier: Apache-2.0
Name:           jansson
Version:        2.15.1
Release:        1%{?dist}
Summary:        C library for encoding, decoding, and manipulating JSON
License:        MIT AND LicenseRef-Public-Domain
URL:            https://jansson.readthedocs.io/
Source0:        jansson-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
Jansson is a C library for encoding, decoding, and manipulating JSON data.
It has no external runtime dependencies and includes a comprehensive test
suite.

%package devel
Summary:        Development files for Jansson
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, the unversioned library link, and pkg-config metadata for developing
applications with Jansson.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libjansson.la

%check
%make_build check

%files
%license LICENSE
%doc CHANGES README.rst
%{_libdir}/libjansson.so.4*

%files devel
%license LICENSE
%{_includedir}/jansson.h
%{_includedir}/jansson_config.h
%{_libdir}/libjansson.so
%{_libdir}/pkgconfig/jansson.pc

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.15.1-1
- Initial openEuler RISC-V package from reviewed Fedora 44 and upstream evidence.
