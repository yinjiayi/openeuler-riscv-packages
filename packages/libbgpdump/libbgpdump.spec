# SPDX-License-Identifier: Apache-2.0
Name:           libbgpdump
Version:        1.6.2
Release:        1%{?dist}
%global upstream_commit 63fe1c50c7d07bb4c57d4fcc690696adc9b3c306
Summary:        BGP MRT dump parsing library and tool
License:        HPND AND GPL-2.0-or-later
URL:            https://github.com/RIPE-NCC/bgpdump
Source0:        libbgpdump-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  bzip2-devel
BuildRequires:  diffutils
BuildRequires:  gcc
BuildRequires:  gzip
BuildRequires:  make
BuildRequires:  zlib-devel

%description
libbgpdump parses MRT and Zebra/Quagga BGP dump files. The package also
provides the bgpdump command-line reader.

%package devel
Summary:        Development files for libbgpdump
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Public C headers and static archive for developing against libbgpdump.
Upstream installs its shared library without a versioned soname, so the
unversioned shared object is in the runtime package.

%prep
%autosetup -n bgpdump-%{upstream_commit} -p1

%build
autoheader
autoconf
%configure
%make_build

%install
%make_install

%check
# Retain all 13 bundled MRT fixtures in the normal and optional -u passes.
BGPDUMP_TEST_UATTR=1 %make_build check

%files
%license COPYING
%doc README ChangeLog
%{_bindir}/bgpdump
%{_libdir}/libbgpdump.so

%files devel
%license COPYING
%{_includedir}/bgpdump_attr.h
%{_includedir}/bgpdump_formats.h
%{_includedir}/bgpdump_lib.h
%{_includedir}/bgpdump_mstream.h
%{_libdir}/libbgpdump.a

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.2-1
- Package the official SHA-256-pinned RIPE NCC tag with complete regression fixtures.
