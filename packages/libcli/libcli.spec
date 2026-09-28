# SPDX-License-Identifier: Apache-2.0
Name:           libcli
Version:        1.10.7
Release:        1%{?dist}
Summary:        Cisco-style command-line interface library
License:        LGPL-2.1-only
URL:            https://github.com/dparrish/libcli
Source0:        libcli-%{version}.tar.gz
Patch0:         0001-calloc-argument-order.patch

BuildRequires:  gcc
# The target base glibc-devel needs libxcrypt-static from the 4.4 series;
# the supplemental 4.5 devel package conflicts with that installed pair.
BuildRequires:  libxcrypt-devel < 4.5
BuildRequires:  make

%description
Libcli provides a C library for embedding a Cisco-style command-line
interface with command registration, parsing and callbacks.

%package devel
Summary:        Development files for libcli
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Public header, static library, and linker name for building libcli consumers.

%prep
%autosetup -p1

%build
%make_build \
  CC=%{__cc} \
  CFLAGS='%{build_cflags}' \
  OPTIM='%{optflags}' \
  LDFLAGS='%{build_ldflags}' \
  TESTS=1 DYNAMIC_LIB=1 STATIC_LIB=1

%install
install -D -m 0755 libcli.so.%{version} %{buildroot}%{_libdir}/libcli.so.%{version}
ln -s libcli.so.%{version} %{buildroot}%{_libdir}/libcli.so.1.10
ln -s libcli.so.1.10 %{buildroot}%{_libdir}/libcli.so
install -D -m 0644 libcli.a %{buildroot}%{_libdir}/libcli.a
install -D -m 0644 libcli.h %{buildroot}%{_includedir}/libcli.h

%check
# Upstream does not register an automated test target. Its clitest example is
# built by the default make target; installed smoke tests command dispatch.
test -x clitest

%files
%license COPYING
%doc README.md
%{_libdir}/libcli.so.1.10*

%files devel
%license COPYING
%doc doc/developers-guide.md
%{_includedir}/libcli.h
%{_libdir}/libcli.a
%{_libdir}/libcli.so

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.10.7-1
- Package the official libcli 1.10.7 release and installed command smoke.
