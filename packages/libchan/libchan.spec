# SPDX-License-Identifier: Apache-2.0
Name:           libchan
Version:        0.0.4
Release:        1%{?dist}
Summary:        Pure C implementation of Go-style channels
License:        Apache-2.0
URL:            https://github.com/tylertreat/chan
Source0:        libchan-0.0.4.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  glibc-devel
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
Pure C implementation of buffered and unbuffered Go-style channels, including
send/receive synchronization, closing, selects and typed value interfaces.

%package devel
Summary:        Headers, shared/static development libraries and original tests
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc
Requires:       glibc-devel
Requires:       bash
Requires:       coreutils
Requires:       binutils
Requires:       gawk
Requires:       grep

%description devel
Public chan and queue headers, default static library and shared-library linker
symlink, plus the unchanged original functional test source and replay driver.
These tests do not establish performance, formal thread safety or native timing.

%prep
%autosetup -n chan-b4120abe5d642284182f04965e793cc918daf711

%build
autoreconf -fi
export CFLAGS="%{optflags} -UNDEBUG"
%configure
%make_build V=1

%install
%make_install
# Preserve the default static library; discard only libtool metadata.
find %{buildroot}%{_libdir} -name '*.la' -delete
install -d %{buildroot}%{_datadir}/%{name}/tests
install -m 0644 src/chan_test.c %{buildroot}%{_datadir}/%{name}/tests/chan_test.c
cat > %{buildroot}%{_datadir}/%{name}/tests/run-original-tests.sh <<'SH'
#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
root=${1:-}
root=${root%%/}
fixtures="$root/usr/share/libchan/tests"
(cd "$fixtures" && sha256sum -c SHA256SUMS)
scratch=$(mktemp -d)
trap 'rm -rf -- "$scratch"' EXIT
unset LD_LIBRARY_PATH
if test -n "$root"; then
    export LD_LIBRARY_PATH="$root/usr/lib64"
fi
for opt in 0 2; do
    for linkage in shared static; do
        binary="$scratch/original-$linkage-O$opt"
        if test "$linkage" = shared; then
            libs=(-L"$root/usr/lib64" -lchan)
        else
            libs=("$root/usr/lib64/libchan.a")
        fi
        # Do not rewrite or replace any original assertion/test function.
        gcc -std=c99 -O"$opt" -UNDEBUG -Wall -Wextra \
            -I"$root/usr/include/chan" "$fixtures/chan_test.c" \
            "${libs[@]}" -pthread -lrt -o "$binary"
        if readelf -d "$binary" | grep -E '\((RPATH|RUNPATH)\)'; then
            echo 'FAIL unexpected embedded runtime path' >&2
            exit 1
        fi
        if test "$linkage" = shared; then
            readelf -d "$binary" | grep -F 'Shared library: [libchan.so.0]'
            loaded=$(ldd "$binary" | awk '$1 == "libchan.so.0" {print $3}')
            test -n "$loaded"
            test "$(readlink -f "$loaded")" = "$(readlink -f "$root/usr/lib64/libchan.so.0.0.0")"
        elif readelf -d "$binary" | grep -F 'Shared library: [libchan.'; then
            echo 'FAIL static libchan replay linked the shared library' >&2
            exit 1
        fi
        timeout 300 "$binary" | tee "$scratch/$linkage-O$opt.log"
        grep -Fx '14 passed' "$scratch/$linkage-O$opt.log"
        echo "PASS original-chan replay linkage=$linkage opt=$opt scope=functional-concurrency"
    done
done
SH
chmod 0755 %{buildroot}%{_datadir}/%{name}/tests/run-original-tests.sh
(cd %{buildroot}%{_datadir}/%{name}/tests && sha256sum chan_test.c run-original-tests.sh > SHA256SUMS)

%check
# Upstream Travis invokes this complete Automake suite; a timeout is a failure.
timeout 300 make -j1 check V=1
# Replays are not additional unique original tests.
bash %{buildroot}%{_datadir}/%{name}/tests/run-original-tests.sh %{buildroot}

%files
%license LICENSE
%doc README.md
%{_libdir}/libchan.so.0
%{_libdir}/libchan.so.0.0.0

%files devel
%{_includedir}/chan/
%{_libdir}/libchan.so
%{_libdir}/libchan.a
%{_datadir}/%{name}/tests/

%changelog
* Fri Oct 16 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.4-1
- Pin official source, preserve default build and complete original tests.
- Verify unchanged original tests against staged and installed libraries.
