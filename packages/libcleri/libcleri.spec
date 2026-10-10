# SPDX-License-Identifier: Apache-2.0
Name:           libcleri
Version:        1.0.2
Release:        1%{?dist}
Summary:        C language parser library
License:        MIT
URL:            https://github.com/cesbit/libcleri
Source0:        libcleri-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pcre2-devel

%description
Libcleri is a C library for constructing grammars and parsing input strings.

%package devel
Summary:        Development files for libcleri
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pcre2-devel

%description devel
Public headers and linker name for building libcleri consumers.

%prep
%autosetup -p1

%build
%make_build -C Release \
  CC=%{__cc} \
  CFLAGS='%{build_cflags}' \
  LDFLAGS='%{build_ldflags}'

%install
install -D -m 0755 Release/libcleri.so %{buildroot}%{_libdir}/libcleri.so.%{version}
ln -s libcleri.so.%{version} %{buildroot}%{_libdir}/libcleri.so.1
ln -s libcleri.so.1 %{buildroot}%{_libdir}/libcleri.so
install -d %{buildroot}%{_includedir}/cleri
install -m 0644 inc/cleri/*.h %{buildroot}%{_includedir}/cleri/

%check
%make_build -C Release -j1 test

%files
%license LICENSE.md
%doc README.md
%{_libdir}/libcleri.so.1*

%files devel
%license LICENSE.md
%{_includedir}/cleri/
%{_libdir}/libcleri.so

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.2-1
- Package official libcleri 1.0.2 with its complete functional test script.
