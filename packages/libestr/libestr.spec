# SPDX-License-Identifier: Apache-2.0
Name:           libestr
Version:        0.1.11
Release:        1%{?dist}
Summary:        Essential string handling library
License:        LGPL-2.1-or-later
URL:            https://libestr.adiscon.com/
Source0:        libestr-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
libestr provides compact string objects and essential string manipulation
helpers used by rsyslog-related projects.

%package devel
Summary:        Development files for libestr
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header, linker name, and pkg-config metadata for developing with libestr.

%prep
%autosetup -p1

%build
autoreconf -fiv
%configure --disable-static --enable-testbench
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la

%check
%make_build check
cat > api-check.c <<'EOF'
#include <stdio.h>
#include <string.h>
#include "libestr.h"
int main(void) {
  es_str_t *s = es_newStrFromCStr("RVA23", 5);
  int ok = s && es_strlen(s) == 5 && es_strbufcmp(s, (const unsigned char *)"RVA23", 5) == 0;
  es_deleteStr(s);
  puts(es_version());
  return ok ? 0 : 1;
}
EOF
%{__cc} %{build_cflags} api-check.c -Iinclude -Lsrc/.libs -Wl,-rpath,$PWD/src/.libs -lestr %{build_ldflags} -o api-check
./api-check | grep -Fx '%{version}'

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/libestr.so.*

%files devel
%{_includedir}/libestr.h
%{_libdir}/libestr.so
%{_libdir}/pkgconfig/libestr.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.11-1
- Initial openEuler RISC-V package with an offline public-API check.
