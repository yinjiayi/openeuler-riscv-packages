# SPDX-License-Identifier: Apache-2.0
Name:           libsodium
Version:        1.0.22
Release:        1%{?dist}
Summary:        Modern and easy-to-use cryptographic library
License:        ISC
URL:            https://libsodium.org/
Source0:        libsodium-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
libsodium provides portable implementations of modern cryptographic primitives.

%package devel
Summary:        Development files for libsodium
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and pkg-config metadata for applications using libsodium.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la

%check
%make_build check

%files
%license LICENSE
%doc AUTHORS ChangeLog README.markdown THANKS
%{_libdir}/libsodium.so.26*

%files devel
%{_includedir}/sodium.h
%{_includedir}/sodium/
%{_libdir}/libsodium.so
%{_libdir}/pkgconfig/libsodium.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.22-1
- Initial openEuler RISC-V package from frozen lineage and official source evidence.
