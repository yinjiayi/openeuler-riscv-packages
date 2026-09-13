# SPDX-License-Identifier: Apache-2.0
Name:           cmark
Version:        0.31.2
Release:        1%{?dist}
Summary:        CommonMark parsing and rendering library and program
License:        BSD-2-Clause AND MIT AND CC-BY-SA-4.0
URL:            https://github.com/commonmark/cmark
Source0:        cmark-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  python3

%description
cmark is the C reference implementation of CommonMark. It provides a command
line renderer and a shared library for parsing, manipulating, and rendering
CommonMark documents.

%package libs
Summary:        Shared library for cmark

%description libs
This package contains the cmark parsing and rendering shared library.

%package devel
Summary:        Development files for cmark
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, pkg-config metadata, CMake metadata, and the unversioned linker name
for cmark.

%package help
Summary:        Documentation for cmark
BuildArch:      noarch

%description help
Manual pages and upstream release documentation for cmark.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install

%check
%ctest --parallel 1

%files
%license COPYING
%{_bindir}/cmark

%files libs
%license COPYING
%{_libdir}/libcmark.so.0.31.2

%files devel
%license COPYING
%{_includedir}/cmark.h
%{_includedir}/cmark_export.h
%{_includedir}/cmark_version.h
%{_libdir}/libcmark.so
%{_libdir}/pkgconfig/libcmark.pc
%{_libdir}/cmake/cmark/

%files help
%license COPYING
%doc README.md changelog.txt
%{_mandir}/man1/cmark.1*
%{_mandir}/man3/cmark.3*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.31.2-1
- Initial openEuler RISC-V package from frozen cross-distribution and upstream evidence.
