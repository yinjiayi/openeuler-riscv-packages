# SPDX-License-Identifier: Apache-2.0
Name:           argtable3
Version:        3.3.1
Release:        1%{?dist}
Summary:        ANSI C command-line parsing library
License:        BSD-3-Clause AND BSD-2-Clause AND TCL
URL:            https://argtable.org
Source0:        argtable3-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  dos2unix
BuildRequires:  gcc
BuildRequires:  make

%description
Argtable3 is a single-library ANSI C toolkit for parsing GNU-style command-line
options. It supplies typed option descriptors, validation, and help output.

%package devel
Summary:        Development files for argtable3
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header, linker name, CMake metadata, and pkg-config metadata for argtable3.

%prep
%autosetup -p1 -n argtable-v%{version}

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DARGTABLE3_ENABLE_TESTS=ON \
  -DARGTABLE3_ENABLE_EXAMPLES=OFF
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE
%doc README.md
%{_libdir}/libargtable3.so.3*

%files devel
%{_includedir}/argtable3.h
%{_libdir}/libargtable3.so
%{_libdir}/cmake/argtable3/
%{_libdir}/pkgconfig/argtable3.pc

%changelog
* Fri Aug 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.3.1-1
- Initial package from the official 3.3.1 release asset.
- Preserve the complete bundled CTest suite in the network-enabled target build.
