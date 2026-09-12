# SPDX-License-Identifier: Apache-2.0
Name:           md4c
Version:        0.5.3
Release:        1%{?dist}
Summary:        Fast C Markdown parser
License:        MIT AND BSD-2-Clause AND CC-BY-SA-4.0
URL:            https://github.com/mity/md4c
Source0:        md4c-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  python3

%description
MD4C is a fast CommonMark-compatible Markdown parser written in C. The
package also provides an HTML renderer and the md2html command-line tool.

%package devel
Summary:        Development files for MD4C
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config and CMake metadata, and unversioned shared-library links
for developing applications with MD4C and its HTML renderer.

%prep
%autosetup -p1 -n md4c-release-%{version}

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_MD2HTML_EXECUTABLE=ON
%cmake_build

%install
%cmake_install

%check
for spec_file in test/spec*.txt; do
  %{__python3} test/run-testsuite.py \
    --program "%{_vpath_builddir}/md2html/md2html" \
    --spec "$spec_file"
done
%{__python3} test/pathological-tests.py \
  --program "%{_vpath_builddir}/md2html/md2html"

%files
%license LICENSE.md test/LICENSE.md
%doc README.md
%{_bindir}/md2html
%{_libdir}/libmd4c.so.0*
%{_libdir}/libmd4c-html.so.0*
%{_mandir}/man1/md2html.1*

%files devel
%license LICENSE.md test/LICENSE.md
%{_includedir}/md4c.h
%{_includedir}/md4c-html.h
%{_libdir}/libmd4c.so
%{_libdir}/libmd4c-html.so
%{_libdir}/pkgconfig/md4c.pc
%{_libdir}/pkgconfig/md4c-html.pc
%{_libdir}/cmake/md4c/

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.5.3-1
- Initial openEuler RISC-V package with complete upstream specification and pathological tests.
