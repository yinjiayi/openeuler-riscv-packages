# SPDX-License-Identifier: Apache-2.0
%global upstream_commit 8d7fe35d2cc0a669af89ca039f506e787a6ebaa6
Name:           libgse
Version:        1.2.1
Release:        1%{?dist}
Summary:        Generic Stream Encapsulation protocol library
License:        LGPL-3.0-or-later AND BSD-4-Clause-UC
URL:            https://github.com/CNES/libgse
Source0:        libgse-1.2.1.tar.gz
Source1:        COPYING.GPL3
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconf
BuildRequires:  libpcap-devel
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  grep
BuildRequires:  sed
BuildRequires:  binutils


%description
Generic Stream Encapsulation protocol library for Linux and Unix systems.
The library encapsulates and de-encapsulates packet data; its offline
tests do not require a network device.

%package devel
Summary:        Development files and offline conformance fixtures for libgse
Requires:       %{name} = %{version}-%{release}
Requires:       gcc
Requires:       libpcap-devel
Requires:       pkgconf
Requires:       bash
Requires:       coreutils
Requires:       binutils

%description devel
Public headers, shared-library linker interface, pkg-config metadata and
an unmodified upstream public-API test with its original offline PCAP input.

%prep
%autosetup -n %{name}-%{upstream_commit}
cp -p %{SOURCE1} COPYING.GPL3

%build
autoreconf -fiv
# Preserve original defaults, including configure/PC version1.2.0 in tag1.2.1.
export CFLAGS="%{optflags} -UNDEBUG"
%configure
%make_build

%install
%make_install docdir=%{_docdir}/%{name}
# Libtool metadata is not a public runtime/development interface.
find %{buildroot} -name '*.la' -delete
install -d %{buildroot}%{_datadir}/%{name}/tests
install -pm0644 test/test_encap_deencap.c test/encap_deencap_max_pdu_length.pcap \
    %{buildroot}%{_datadir}/%{name}/tests/
sha256sum test/test_encap_deencap.c test/encap_deencap_max_pdu_length.pcap \
    | sed 's|  test/|  |' > %{buildroot}%{_datadir}/%{name}/tests/SHA256SUMS
cat > %{buildroot}%{_datadir}/%{name}/tests/run-contract.sh <<'SH'
#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
root=${1:-}
test -z "$root" || test -d "$root/usr/lib64"
fixtures="$root/usr/share/libgse/tests"
cd "$fixtures"
sha256sum -c SHA256SUMS
export PKG_CONFIG_LIBDIR="$root/usr/lib64/pkgconfig"
export PKG_CONFIG_SYSROOT_DIR="$root"
test "$(pkg-config --modversion gse)" = 1.2.0
expected=$(readlink -f "$root/usr/lib64/libgse.so.0")
test -s "$expected"
workdir=$(mktemp -d /tmp/libgse-contract.XXXXXXXX)
trap 'rm -f "$workdir/test-0" "$workdir/test-2"; rmdir "$workdir"' EXIT
if test -n "$root"; then
    export LD_LIBRARY_PATH="$root/usr/lib64"
else
    unset LD_LIBRARY_PATH
fi
for opt in 0 2; do
    gcc -O"$opt" -g -UNDEBUG -Wall -Wextra -I"$root/usr/include/gse" \
        $(pkg-config --cflags gse) test_encap_deencap.c \
        -o "$workdir/test-$opt" $(pkg-config --libs gse) -lpcap -pthread
    readelf -d "$workdir/test-$opt" | grep -F 'Shared library: [libgse.so.0]'
    if readelf -d "$workdir/test-$opt" | grep -E '\((RPATH|RUNPATH)\)'; then
        echo 'Unexpected embedded library search path' >&2
        exit 1
    fi
    actual=$(ldd "$workdir/test-$opt" | awk '$1 == "libgse.so.0" {print $3}')
    test -n "$actual"
    test "$(readlink -f "$actual")" = "$expected"
    # Original argument0 first; other sizes are explicitly downstream checks.
    # No upstream shell-wrapper verbose retry: fail on the first nonzero result.
    for fragment in 0 1400 4096; do
        "$workdir/test-$opt" "$fragment" encap_deencap_max_pdu_length.pcap
        echo "PASS downstream-libgse opt=$opt fragment=$fragment"
    done
done
echo 'PASS downstream-libgse total=6 original-public-source=unchanged'
SH
chmod 0755 %{buildroot}%{_datadir}/%{name}/tests/run-contract.sh

%check
# All32 original registered scripts/19 check programs, unchanged shell wrappers.
make -j1 check VERBOSE=1
# Separate staged public-header/shared-library semantic replay, not upstream count.
bash %{buildroot}%{_datadir}/%{name}/tests/run-contract.sh %{buildroot}

%files
%license COPYING.LESSER COPYING.GPL3 COPYING.BSD
%{_docdir}/%{name}/
%{_libdir}/libgse.so.*

%files devel
%{_includedir}/gse/
%{_libdir}/libgse.so
%{_libdir}/pkgconfig/gse.pc
%{_datadir}/%{name}/tests/

%changelog
* Thu Oct 15 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.1-1
- Package fixed CNES release with all original defaults and offline tests.
- Preserve original1.2.0 PC version and add distinct installed public-API replay.
