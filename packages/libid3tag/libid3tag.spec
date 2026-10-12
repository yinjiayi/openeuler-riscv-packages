# SPDX-License-Identifier: Apache-2.0
Name:           libid3tag
Version:        0.16.4
Release:        1%{?dist}
Summary:        Library for reading and writing ID3 tags
License:        GPL-2.0-or-later
URL:            https://codeberg.org/tenacityteam/libid3tag
Source0:        libid3tag-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gperf
BuildRequires:  make
BuildRequires:  pkgconf
BuildRequires:  zlib-devel

%description
libid3tag reads and renders ID3v1 and ID3v2 metadata tags in audio files.

%package devel
Summary:        Development files for libid3tag
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf
Requires:       zlib-devel

%description devel
The public header, unversioned linker name, pkg-config metadata, and CMake
package configuration for developing applications with libid3tag.

%prep
%autosetup -n libid3tag -p1

%build
%cmake_conf -DBUILD_SHARED_LIBS=ON
%cmake_build

%install
%cmake_install

%check
# No upstream test target is registered; verify the public ID3v1 rendering
# and parsing APIs with the freshly built shared library.
cat > id3tag-api-check.c <<'EOF'
#include <id3tag.h>
#include <string.h>

int main(void) {
    struct id3_tag *tag = id3_tag_new();
    struct id3_tag *parsed;
    id3_byte_t data[128], rendered[128];
    if (!tag) return 1;
    if (id3_tag_options(tag, ID3_TAG_OPTION_ID3V1, ID3_TAG_OPTION_ID3V1) < 0) return 2;
    if (id3_tag_render(tag, data) != sizeof data) return 3;
    if (memcmp(data, "TAG", 3) != 0) return 4;
    parsed = id3_tag_parse(data, sizeof data);
    if (!parsed) return 5;
    if (id3_tag_render(parsed, rendered) != sizeof rendered) return 6;
    if (memcmp(data, rendered, sizeof data) != 0) return 7;
    id3_tag_delete(parsed);
    id3_tag_delete(tag);
    return 0;
}
EOF
gcc %{optflags} -I%{_vpath_builddir} id3tag-api-check.c \
  -L%{_vpath_builddir} -Wl,-rpath,$PWD/%{_vpath_builddir} -lid3tag -lz \
  -o id3tag-api-check
./id3tag-api-check

%files
%license COPYRIGHT COPYING
%doc README.md CHANGES
%{_libdir}/libid3tag.so.0*

%files devel
%license COPYRIGHT COPYING
%{_includedir}/id3tag.h
%{_libdir}/libid3tag.so
%{_libdir}/pkgconfig/id3tag.pc
%{_libdir}/cmake/id3tag/

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.16.4-1
- Initial openEuler RISC-V package with public ID3v1 API tests.
