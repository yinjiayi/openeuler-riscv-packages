# SPDX-License-Identifier: Apache-2.0
Name:           libbitarray
Version:        2.0
Release:        1%{?dist}
Summary:        Resizable bit arrays and bit-lock primitives for C
License:        CC0-1.0
URL:            https://github.com/noporpoise/BitArray
Source0:        libbitarray-%{version}.tar.gz

BuildRequires:  binutils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
BitArray implements resizable arrays of bits and bit-lock primitives.

%package devel
Summary:        Development files for BitArray
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and static and shared link names for BitArray consumers.

%prep
%autosetup -n BitArray-%{version}

%build
%make_build all CC=%{__cc} CXX=%{__cxx} \
  CFLAGS='%{build_cflags} -Wall -Wextra -I.. -I. -L..'
%{__cc} %{build_ldflags} -shared -Wl,-soname,libbitarr.so.2 \
  -o libbitarr.so.2.0.0 bit_array.o

%install
install -D -m 0755 libbitarr.so.2.0.0 %{buildroot}%{_libdir}/libbitarr.so.2.0.0
ln -s libbitarr.so.2.0.0 %{buildroot}%{_libdir}/libbitarr.so.2
ln -s libbitarr.so.2 %{buildroot}%{_libdir}/libbitarr.so
install -D -m 0644 libbitarr.a %{buildroot}%{_libdir}/libbitarr.a
install -D -m 0644 bit_array.h %{buildroot}%{_includedir}/bit_array.h
install -D -m 0644 bit_macros.h %{buildroot}%{_includedir}/bit_macros.h
install -D -m 0644 bar.h %{buildroot}%{_includedir}/bar.h

%check
%make_build test
./dev/bitlock_try_test

%files
%license LICENSE
%doc AUTHORS README.md
%{_libdir}/libbitarr.so.2*

%files devel
%license LICENSE
%{_includedir}/bit_array.h
%{_includedir}/bit_macros.h
%{_includedir}/bar.h
%{_libdir}/libbitarr.so
%{_libdir}/libbitarr.a

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0-1
- Package official BitArray 2.0 with full upstream tests and installed smoke.
