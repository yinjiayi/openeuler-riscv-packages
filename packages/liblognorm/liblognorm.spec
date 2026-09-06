# SPDX-License-Identifier: Apache-2.0
Name:           liblognorm
Version:        2.1.0
Release:        1%{?dist}
Summary:        Fast log message normalization library
License:        Apache-2.0 AND LGPL-2.1-or-later
URL:            https://www.liblognorm.com/
Source0:        liblognorm-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  libestr-devel
BuildRequires:  libfastjson-devel
BuildRequires:  make
BuildRequires:  pcre2-devel
BuildRequires:  pkgconf

%description
liblognorm parses unstructured log messages into normalized structured data
using reusable rulebases and supports legacy, regular-expression, and TurboVM
matching engines.

%package devel
Summary:        Development files for liblognorm
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Public headers, pkg-config metadata, and the unversioned linker name for
liblognorm.

%package utils
Summary:        Command-line utility for liblognorm
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description utils
The lognormalizer command-line rulebase test and message normalization tool.

%package help
Summary:        Documentation for liblognorm
BuildArch:      noarch

%description help
Upstream release, contributor, and usage documentation for liblognorm.

%prep
%autosetup -p1

%build
%configure \
  --disable-static \
  --enable-regexp \
  --enable-testbench \
  --enable-advanced-stats \
  --enable-tools \
  --enable-turbo \
  --disable-docs
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la

%check
%make_build check

%files
%license COPYING COPYING.ASL20
%{_libdir}/liblognorm.so.5*

%files devel
%license COPYING COPYING.ASL20
%{_includedir}/liblognorm.h
%{_includedir}/lognorm-features.h
%{_includedir}/lognorm-turbo.h
%{_libdir}/liblognorm.so
%{_libdir}/pkgconfig/lognorm.pc

%files utils
%license COPYING COPYING.ASL20
%{_bindir}/lognormalizer

%files help
%license COPYING COPYING.ASL20
%doc AGENTS.md AUTHORS ChangeLog NEWS README

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.0-1
- Initial openEuler RISC-V package from frozen cross-distribution and upstream evidence.
