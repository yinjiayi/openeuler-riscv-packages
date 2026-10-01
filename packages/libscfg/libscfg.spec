# SPDX-License-Identifier: Apache-2.0
Name:           libscfg
Version:        0.2.0
Release:        1%{?dist}
Summary:        C library for the scfg configuration format
License:        MIT
URL:            https://codeberg.org/emersion/libscfg
Source0:        libscfg-v%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf-pkg-config

%description
libscfg parses and formats the scfg configuration-file format from C.

%package devel
Summary:        Development files for libscfg
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The public header, pkg-config metadata, and linker name for libscfg.

%prep
%autosetup -n libscfg

%build
%meson
%meson_build

%install
%meson_install

%check
# Upstream registers exactly two fail-closed cases: parse and format.
%meson_test

%files
%license LICENSE
%doc README.md
%{_libdir}/libscfg.so.0.2.0
%{_libdir}/libscfg.so.2

%files devel
%license LICENSE
%{_includedir}/scfg.h
%{_libdir}/libscfg.so
%{_libdir}/pkgconfig/scfg.pc

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.0-1
- Package official libscfg and retain both upstream Meson tests.
