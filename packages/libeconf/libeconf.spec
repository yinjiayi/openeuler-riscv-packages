# SPDX-License-Identifier: Apache-2.0
Name:           libeconf
Version:        0.8.4
Release:        1%{?dist}
Summary:        Configuration-file parser and merge library
License:        MIT
URL:            https://opensuse.github.io/libeconf/
Source0:        libeconf-%{version}.tar.gz

BuildRequires:  bash
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
libeconf reads key-value configuration files and merges vendor, runtime, and
administrator overrides. It also provides the econftool command-line utility.

%package devel
Summary:        Development files for libeconf
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Public headers, linker name, pkg-config metadata, CMake metadata, and API manuals.

%prep
%autosetup -n libeconf-4f951d11b1ec5dcea9fd6b4fbe192226d93050c5

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_TESTS=ON \
  -DBUILD_DOCUMENTATION=OFF
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE
%doc README.md
%{_bindir}/econftool
%{_libdir}/libeconf.so.0*
%{_mandir}/man8/econftool.8*

%files devel
%license LICENSE
%{_includedir}/libeconf.h
%{_includedir}/libeconf_ext.h
%{_libdir}/libeconf.so
%{_libdir}/pkgconfig/libeconf.pc
%{_libdir}/cmake/libeconf/
%{_mandir}/man3/*.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.4-1
- Package the official stable libeconf 0.8.4 commit with all 48 upstream tests.
