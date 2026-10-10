# SPDX-License-Identifier: Apache-2.0
Name:           libebml
Version:        1.4.6
Release:        1%{?dist}
Summary:        C++ library for Extensible Binary Meta Language
License:        LGPL-2.1-or-later AND BSL-1.0
URL:            https://www.matroska.org/
Source0:        libebml-%{version}.tar.xz
Source1:        utfcpp-3.2.5.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconf

%description
LibEBML is a C++ library for reading and writing Extensible Binary Meta
Language structures used by Matroska.

%package devel
Summary:        Development files for LibEBML
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, the unversioned library link, pkg-config metadata, and CMake
configuration for applications using LibEBML.

%prep
%autosetup -n libebml-%{version} -a 1 -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DFETCHCONTENT_SOURCE_DIR_UTF8CPP="$PWD/utfcpp-3.2.5"
%cmake_build

%install
%cmake_install

%check
cat > %{_vpath_builddir}/ebml-smoke.cpp <<'EOF'
#include <ebml/EbmlId.h>
#include <ebml/EbmlVersion.h>
#include <cstring>
#include <iostream>

int main() {
    const libebml::EbmlId id(0x1A45DFA3u, 4);
    binary bytes[4] = {};
    id.Fill(bytes);
    if (LIBEBML_VERSION != 0x010406 || id.GetLength() != 4 ||
        bytes[0] != 0x1a || bytes[1] != 0x45 ||
        bytes[2] != 0xdf || bytes[3] != 0xa3 ||
        libebml::EbmlCodeVersion.empty()) return 1;
    std::cout << "libebml-api-ok\n";
    return 0;
}
EOF
g++ -std=c++14 -I. -I%{_vpath_builddir} \
  %{_vpath_builddir}/ebml-smoke.cpp -L%{_vpath_builddir} -lebml \
  -o %{_vpath_builddir}/ebml-smoke
LD_LIBRARY_PATH="$PWD/%{_vpath_builddir}" %{_vpath_builddir}/ebml-smoke | grep -Fx 'libebml-api-ok'

%files
%license LICENSE.LGPL utfcpp-3.2.5/LICENSE
%doc NEWS.md README.md
%{_libdir}/libebml.so.5*

%files devel
%license LICENSE.LGPL utfcpp-3.2.5/LICENSE
%{_includedir}/ebml/
%{_libdir}/libebml.so
%{_libdir}/cmake/EBML/
%{_libdir}/pkgconfig/libebml.pc

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.6-1
- Package the official LibEBML 1.4.6 release for openEuler RISC-V.
