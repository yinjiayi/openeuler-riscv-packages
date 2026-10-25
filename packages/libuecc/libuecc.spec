# SPDX-License-Identifier: Apache-2.0
Name:           libuecc
Version:        7
Release:        1%{?dist}
%global upstream_commit 7c9a6f6af088d0764e792cf849e553d7f55ff99e
Summary:        Small Ed25519-compatible elliptic-curve library
License:        BSD-2-Clause
URL:            https://github.com/neocturne/libuecc
Source0:        libuecc-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  pkgconf

%description
libuecc provides a small C implementation of elliptic-curve point and field
operations compatible with the Ed25519 representation.

%package devel
Summary:        Development files for libuecc
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Public C header, pkg-config metadata, unversioned linker name, and static
library for developing applications with libuecc.

%prep
%autosetup -n libuecc-%{upstream_commit} -p1

%build
%cmake_conf -DLIB_SUFFIX=64
%cmake_build

%install
%cmake_install

%check
# Upstream v7 has no registered tests; check deterministic public-API properties.
cat > libuecc-api-check.c <<'EOF'
#include <libuecc/ecc.h>
#include <stdint.h>
#include <string.h>

static int equal_packed(const ecc_25519_work_t *left,
                        const ecc_25519_work_t *right) {
    ecc_int256_t a, b;
    ecc_25519_store_packed_ed25519(&a, left);
    ecc_25519_store_packed_ed25519(&b, right);
    return memcmp(a.p, b.p, sizeof(a.p)) == 0;
}

int main(void) {
    ecc_25519_work_t loaded, once, twice, doubled, inverse, zero;
    ecc_int256_t packed, one = {{1}};
    ecc_25519_store_packed_ed25519(&packed, &ecc_25519_work_default_base);
    if (packed.p[0] != 0x58) return 1;
    for (unsigned i = 1; i < sizeof(packed.p); ++i)
        if (packed.p[i] != 0x66) return 2;
    if (!ecc_25519_load_packed_ed25519(&loaded, &packed)) return 3;
    if (!equal_packed(&loaded, &ecc_25519_work_default_base)) return 4;
    ecc_25519_scalarmult_base(&once, &one);
    if (!equal_packed(&once, &ecc_25519_work_default_base)) return 5;
    ecc_25519_add(&twice, &once, &once);
    ecc_25519_double(&doubled, &once);
    if (!equal_packed(&twice, &doubled)) return 6;
    ecc_25519_negate(&inverse, &once);
    ecc_25519_add(&zero, &once, &inverse);
    return ecc_25519_is_identity(&zero) ? 0 : 7;
}
EOF
${CC:-cc} %{optflags} -Iinclude libuecc-api-check.c \
  -L%{_vpath_builddir}/src -luecc -o libuecc-api-check
LD_LIBRARY_PATH="$PWD/%{_vpath_builddir}/src${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" ./libuecc-api-check

%files
%license COPYRIGHT
%doc README CHANGELOG
%{_libdir}/libuecc.so.0*

%files devel
%license COPYRIGHT
%{_includedir}/libuecc-%{version}/
%{_libdir}/libuecc.so
%{_libdir}/libuecc.a
%{_libdir}/pkgconfig/libuecc.pc

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 7-1
- Initial package from the official SHA-256-pinned libuecc v7 source.
