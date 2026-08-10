# SPDX-License-Identifier: Apache-2.0
Name:           marisa
Version:        0.3.1
Release:        1%{?dist}
Summary:        Matching Algorithm with Recursively Implemented StorAge trie
License:        BSD-2-Clause OR LGPL-2.1-or-later
URL:            https://github.com/s-yata/marisa-trie
Source0:        marisa-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make

%description
MARISA is a compact static trie implementation with tools for constructing,
querying, inspecting, and benchmarking dictionaries.

%package devel
Summary:        Development files for MARISA
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config and CMake metadata, and the unversioned library link for
developing applications with MARISA.

%prep
%autosetup -p1 -n marisa-trie-%{version}

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_TESTING=ON \
  -DENABLE_NATIVE_CODE=OFF \
  -DENABLE_TOOLS=ON \
  -DLIB_INSTALL_DIR=%{_lib}
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license COPYING.md
%doc AUTHORS README.md
%{_bindir}/marisa-*
%{_libdir}/libmarisa.so.0*

%files devel
%license COPYING.md
%{_includedir}/marisa.h
%{_includedir}/marisa/
%{_libdir}/libmarisa.so
%{_libdir}/pkgconfig/marisa.pc
%{_libdir}/cmake/Marisa/

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.1-1
- Initial openEuler RISC-V package.
