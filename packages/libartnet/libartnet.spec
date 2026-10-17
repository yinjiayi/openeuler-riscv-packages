# SPDX-License-Identifier: Apache-2.0
Name:           libartnet
Version:        1.2.0
Release:        1%{?dist}
Summary:        ArtNet protocol implementation for DMX over IP
License:        LGPL-2.1-or-later
URL:            https://github.com/atlesn/libartnet
Source0:        libartnet-1.2.0.tar.gz
Patch0:         0001-fix-configure-and-pkgconfig-contract.patch
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  glibc-devel
BuildRequires:  pkgconf
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  binutils
BuildRequires:  gzip
BuildRequires:  tar
BuildRequires:  gawk
BuildRequires:  grep
BuildRequires:  sed
BuildRequires:  findutils
BuildRequires:  diffutils
BuildRequires:  rpm

%description
An implementation of the ArtNet protocol for transmitting DMX data over IP.

%package devel
Summary:        Headers and development libraries for libartnet
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc
Requires:       glibc-devel
Requires:       pkgconf
Requires:       bash
Requires:       coreutils
Requires:       binutils
Requires:       grep
Requires:       gawk

%description devel
Public headers, default static library, shared-library linker symlink,
pkg-config metadata and limited offline ABI/argument-contract test fixtures.
These fixtures do not validate ArtNet network or DMX interoperability.

%prep
%autosetup -n libartnet-416a83e92d150e8e0295a9aabd7ad1fb1c1689bc -p1

%build
autoreconf -fi
export CFLAGS="%{optflags} -UNDEBUG"
%configure
%make_build V=1

%install
%make_install
# Remove only libtool's installed metadata, not the default static library.
find %{buildroot}%{_libdir} -name '*.la' -delete
install -d %{buildroot}%{_datadir}/%{name}/tests
cat > %{buildroot}%{_datadir}/%{name}/tests/contract.c <<'C'
/* SPDX-License-Identifier: Apache-2.0 */
#ifdef NDEBUG
#error Assertions must not be disabled
#endif
#include <artnet/artnet.h>
#include <artnet/packets.h>
#include <sys/socket.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static unsigned checks;
#define CHECK(expr) do { ++checks; if (!(expr)) { \
    fprintf(stderr, "FAIL downstream-artnet line=%d: %s\n", __LINE__, #expr); \
    exit(1); } } while (0)
int main(void) {
    int domain = -1, type = -1, protocol = -1;
    artnet_node_config_t config;
    fd_set fds;
    memset(&config, 0, sizeof(config));
    FD_ZERO(&fds);
    CHECK(ARTNET_MAX_PORTS == 4);
    CHECK(ARTNET_MAX_PAGES == 256);
    CHECK(ARTNET_SHORT_NAME_LENGTH == 18);
    CHECK(ARTNET_LONG_NAME_LENGTH == 64);
    CHECK(ARTNET_DMX_LENGTH == 512);
    CHECK(ARTNET_ADDRESS_NO_CHANGE == 0x7f);
    artnet_get_sockopt(&domain, &type, &protocol);
    CHECK(domain == PF_INET);
    CHECK(type == SOCK_DGRAM);
    CHECK(protocol == 0);
    CHECK(artnet_start(NULL) == ARTNET_EARG);
    CHECK(artnet_strerror() != NULL && strlen(artnet_strerror()) > 0);
    CHECK(artnet_stop(NULL) == ARTNET_EARG);
    CHECK(artnet_destroy(NULL) == ARTNET_EARG);
    CHECK(artnet_read(NULL, 0) == ARTNET_EARG);
    CHECK(artnet_setoem(NULL, 0, 1) == ARTNET_EARG);
    CHECK(artnet_setesta(NULL, 0, 1) == ARTNET_EARG);
    CHECK(artnet_set_bcast_limit(NULL, 0) == ARTNET_EARG);
    CHECK(artnet_set_node_type(NULL, ARTNET_NODE) == ARTNET_EARG);
    CHECK(artnet_set_short_name(NULL, "offline") == ARTNET_EARG);
    CHECK(artnet_set_long_name(NULL, "offline ABI contract") == ARTNET_EARG);
    CHECK(artnet_set_port_type(NULL, 0, 0, ARTNET_ENABLE_OUTPUT, ARTNET_PORT_DMX) == ARTNET_EARG);
    CHECK(artnet_set_subnet_addr(NULL, 1) == ARTNET_EARG);
    CHECK(artnet_set_net_addr(NULL, 1) == ARTNET_EARG);
    CHECK(artnet_get_universe_addr(NULL, 0, 0, ARTNET_OUTPUT_PORT) == ARTNET_EARG);
    CHECK(artnet_get_config(NULL, &config) == ARTNET_EARG);
    CHECK(artnet_set_fdset(NULL, &fds) == ARTNET_EARG);
    CHECK(artnet_get_nl(NULL) == NULL);
    CHECK(artnet_nl_first(NULL) == NULL);
    CHECK(artnet_nl_next(NULL) == NULL);
    CHECK(artnet_nl_get_length(NULL) == 0);
    printf("PASS downstream-artnet checks=%u skips=0 scope=offline-ABI-arguments\n", checks);
    return 0;
}
C
cat > %{buildroot}%{_datadir}/%{name}/tests/run-contract.sh <<'SH'
#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
root=${1:-}
root=${root%%/}
fixtures="$root/usr/share/libartnet/tests"
(cd "$fixtures" && sha256sum -c SHA256SUMS)
scratch=$(mktemp -d)
trap 'rm -rf -- "$scratch"' EXIT
unset PKG_CONFIG_PATH PKG_CONFIG_SYSROOT_DIR LD_LIBRARY_PATH
export PKG_CONFIG_LIBDIR="$root/usr/lib64/pkgconfig"
if test -n "$root"; then
    export PKG_CONFIG_SYSROOT_DIR="$root"
    export LD_LIBRARY_PATH="$root/usr/lib64"
fi
test "$(pkg-config --modversion libartnet)" = 1.2.0
# Implementations differ on sysroot rewriting for --variable output.
# Both forms must resolve to the original /usr prefix, never another directory.
inc=$(pkg-config --variable=includedir libartnet)
lib=$(pkg-config --variable=libdir libartnet)
test "$inc" = /usr/include || test "$inc" = "$root/usr/include"
test "$lib" = /usr/lib64 || test "$lib" = "$root/usr/lib64"
read -r -a flags <<< "$(pkg-config --cflags --libs libartnet)"
for opt in 0 2; do
    gcc -std=gnu11 -O"$opt" -UNDEBUG -Wall -Wextra -Werror \
        "$fixtures/contract.c" "${flags[@]}" -o "$scratch/contract-O$opt"
    readelf -d "$scratch/contract-O$opt" | grep -F 'Shared library: [libartnet.so.1]'
    if readelf -d "$scratch/contract-O$opt" | grep -E '\((RPATH|RUNPATH)\)'; then
        echo 'FAIL unexpected embedded runtime path' >&2
        exit 1
    fi
    loaded=$(ldd "$scratch/contract-O$opt" | awk '$1 == "libartnet.so.1" {print $3}')
    test -n "$loaded"
    test "$(readlink -f "$loaded")" = "$(readlink -f "$root/usr/lib64/libartnet.so.1.0.0")"
    "$scratch/contract-O$opt"
done
SH
chmod 0755 %{buildroot}%{_datadir}/%{name}/tests/run-contract.sh
(cd %{buildroot}%{_datadir}/%{name}/tests && sha256sum contract.c run-contract.sh > SHA256SUMS)

%check
# Preserve the original default check target; upstream registers no test suite.
make check V=1
bash %{buildroot}%{_datadir}/%{name}/tests/run-contract.sh %{buildroot}

%files
%license COPYING
%doc README
%{_libdir}/libartnet.so.1*

%files devel
%license COPYING
%{_includedir}/artnet/
%{_libdir}/libartnet.so
%{_libdir}/libartnet.a
%{_libdir}/pkgconfig/libartnet.pc
%{_datadir}/%{name}/tests/

%changelog
* Thu Oct 15 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.0-1
- Pin official release; preserve default build/check and add limited offline consumer.
- Correct generic configure probe and pkg-config include-root contract.
