# SPDX-License-Identifier: Apache-2.0
Name:           libbloom
Version:        2.0
Release:        1%{?dist}
Summary:        Small C Bloom filter library
License:        BSD-2-Clause AND MIT
URL:            https://github.com/jvirkki/libbloom
Source0:        libbloom-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
Libbloom provides a small C implementation of Bloom filters.

%package devel
Summary:        Development files for libbloom
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header, static library, and unversioned linker name for libbloom.

%prep
%autosetup -p1

%build
%make_build OPT='%{optflags}' LDFLAGS='%{build_ldflags}'

%install
install -D -m 0755 build/libbloom.so.2.0 %{buildroot}%{_libdir}/libbloom.so.2.0
ln -s libbloom.so.2.0 %{buildroot}%{_libdir}/libbloom.so.2
ln -s libbloom.so.2 %{buildroot}%{_libdir}/libbloom.so
install -D -m 0644 build/libbloom.a %{buildroot}%{_libdir}/libbloom.a
install -D -m 0644 bloom.h %{buildroot}%{_includedir}/bloom.h

%check
%make_build -j1 OPT='%{optflags}' LDFLAGS='%{build_ldflags}' test

%files
%license LICENSE murmur2/README
%doc README ChangeLog
%{_libdir}/libbloom.so.2*

%files devel
%license LICENSE murmur2/README
%{_includedir}/bloom.h
%{_libdir}/libbloom.a
%{_libdir}/libbloom.so

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0-1
- Package the official libbloom 2.0 tag with upstream tests.
