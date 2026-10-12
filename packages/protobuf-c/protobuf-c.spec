# SPDX-License-Identifier: Apache-2.0
Name:           protobuf-c
Version:        1.5.2
Release:        1%{?dist}
Summary:        C implementation of Protocol Buffers
License:        BSD-2-Clause
URL:            https://github.com/protobuf-c/protobuf-c
Source0:        protobuf-c-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconf
BuildRequires:  protobuf-compiler
BuildRequires:  protobuf-devel
BuildRequires:  valgrind
Provides:       protobuf-c-compiler = %{version}-%{release}

%description
protobuf-c provides a C runtime and a protoc plug-in for encoding and
decoding data described with the Protocol Buffers schema language.

%package devel
Summary:        Development files for protobuf-c
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       protobuf-c-compiler = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, schema support, pkg-config metadata, and the unversioned linker
name for developing C applications with Protocol Buffers.

%prep
%autosetup -p1

%build
%configure \
  --disable-static \
  --enable-valgrind-tests
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libprotobuf-c.la

%check
%make_build check

%files
%license LICENSE
%doc CHANGELOG.md README.md
%{_bindir}/protoc-c
%{_bindir}/protoc-gen-c
%{_libdir}/libprotobuf-c.so.1*

%files devel
%license LICENSE
%{_includedir}/google/protobuf-c/protobuf-c.h
%{_includedir}/protobuf-c/protobuf-c.h
%{_includedir}/protobuf-c/protobuf-c.proto
%{_libdir}/libprotobuf-c.so
%{_libdir}/pkgconfig/libprotobuf-c.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.2-1
- Update protobuf-c for openEuler RISC-V from Fedora 44 and frozen cross-distribution evidence.
