# SPDX-License-Identifier: Apache-2.0
Name:           libpsl
Version:        0.23.3
Release:        1%{?dist}
Summary:        C library for the Public Suffix List
License:        BSD-3-Clause AND MIT AND MPL-2.0
URL:            https://rockdaboot.github.io/libpsl/
Source0:        libpsl-0.23.3.tar.gz

BuildRequires:  gcc
BuildRequires:  libidn2-devel
BuildRequires:  libunistring-devel
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf
BuildRequires:  python3

%description
libpsl provides fast and thread-safe queries over the Public Suffix List for
cookie validation, registrable-domain discovery, and related web use cases.

%package utils
Summary:        Public Suffix List command-line utilities
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python3

%description utils
The psl exploration utility and the psl-make-dafsa data compiler.

%package devel
Summary:        Development files for libpsl
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, pkg-config metadata, and the unversioned linker name for libpsl.

%package help
Summary:        Documentation for libpsl
BuildArch:      noarch

%description help
Manual pages and upstream release documentation for libpsl.

%prep
%autosetup -p1

%build
%meson \
  -Dbuiltin=true \
  -Ddocs=false \
  -Druntime=libidn2 \
  -Dtests=true
%meson_build

%install
%meson_install

%check
%meson_test

%files
%license COPYING LICENSE src/LICENSE.chromium
%{_libdir}/libpsl.so.5*

%files utils
%license COPYING LICENSE src/LICENSE.chromium
%{_bindir}/psl
%{_bindir}/psl-make-dafsa

%files devel
%license COPYING LICENSE src/LICENSE.chromium
%{_includedir}/libpsl.h
%{_libdir}/libpsl.so
%{_libdir}/pkgconfig/libpsl.pc

%files help
%license COPYING LICENSE src/LICENSE.chromium
%doc AUTHORS ChangeLog NEWS README.md
%{_mandir}/man1/psl.1*
%{_mandir}/man1/psl-make-dafsa.1*

%changelog
* Mon Aug 24 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.23.3-1
- Track the upstream README.md rename in the help package manifest.

* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.23.1-1
- Initial openEuler RISC-V package from frozen cross-distribution and upstream evidence.
