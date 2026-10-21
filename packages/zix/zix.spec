# SPDX-License-Identifier: Apache-2.0
Name:           zix
Version:        0.8.2
Release:        1%{?dist}
Summary:        Portability wrappers and data structures for C
License:        0BSD OR ISC
URL:            https://drobilla.net/software/zix.html
Source0:        zix-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  python3

%description
Zix is a lightweight C library of portability wrappers, allocation helpers,
data structures, threading primitives, and filesystem utilities.

%package devel
Summary:        Development files for Zix
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and the unversioned library link for developing
applications with Zix.

%prep
%autosetup -p1

%build
%meson \
  --wrap-mode=nodownload \
  -Dbenchmarks=disabled \
  -Dchecks=enabled \
  -Ddocs=disabled \
  -Dlint=false \
  -Dposix=enabled \
  -Dtests=enabled \
  -Dtests_cpp=enabled \
  -Dthreads=enabled
%meson_build

%install
%meson_install

%check
%meson_test

%files
%license COPYING LICENSES/0BSD.txt LICENSES/ISC.txt
%doc NEWS README.md
%{_libdir}/libzix-0.so.0*

%files devel
%license COPYING LICENSES/0BSD.txt LICENSES/ISC.txt
%{_includedir}/zix-0/
%{_libdir}/libzix-0.so
%{_libdir}/pkgconfig/zix-0.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.2-1
- Initial openEuler RISC-V package with the complete shipped upstream tests.
