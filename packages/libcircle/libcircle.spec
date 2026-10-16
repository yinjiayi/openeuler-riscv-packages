# SPDX-License-Identifier: Apache-2.0
Name:           libcircle
Version:        0.3
Release:        1%{?dist}
Summary:        MPI-based distributed work queue library
License:        LicenseRef-LANL-BSD AND BSD-3-Clause AND FSFAP
URL:            https://github.com/hpc/libcircle
Source0:        libcircle-0.3.tar.gz
Patch0:         patches/0001-declare-standard-size-and-string-interfaces.patch
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconf
BuildRequires:  glibc-devel
BuildRequires:  openmpi-devel = 4.1.5-7.oe2403sp3
BuildRequires:  check-devel = 0.15.2-2.oe2403sp3
BuildRequires:  libxcrypt-devel = 4.4.36-3.oe2403sp3
BuildRequires:  patch
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  binutils
BuildRequires:  gzip
BuildRequires:  tar
BuildRequires:  grep
BuildRequires:  gawk
BuildRequires:  sed
BuildRequires:  findutils
BuildRequires:  diffutils
BuildRequires:  rpm


%description
MPI-based automatically distributed global work queue library. This recipe
preserves MPI, default shared/static libraries and the complete upstream queue
test suite. Singleton functional checks are not distributed or native validation.

%package devel
Summary:        Public header, development libraries and original queue tests
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc
Requires:       glibc-devel
Requires:       openmpi-devel = 4.1.5-7.oe2403sp3
Requires:       check-devel = 0.15.2-2.oe2403sp3
Requires:       libxcrypt-devel = 4.4.36-3.oe2403sp3
Requires:       pkgconf
Requires:       bash
Requires:       coreutils
Requires:       binutils
Requires:       gawk
Requires:       grep

%description devel
Public libcircle header, pkg-config metadata, shared-library linker symlink and
default static archive, with the declaration-only patched original Check queue
test source and a staged/installed-library replay driver.

%prep
%setup -q -n libcircle-3d8fbfae2b95fafe71a309fcfbb7c1c993f16ad8
%patch -P 0 -p1

%build
autoreconf -fi
export CFLAGS="%{optflags} -UNDEBUG"
# This is the upstream Travis test-enabled configuration; MPI is mandatory.
%configure --enable-tests
%make_build V=1

%install
%make_install
# Keep the default static library; only discard libtool metadata.
find %{buildroot}%{_libdir} -name '*.la' -delete
install -d %{buildroot}%{_datadir}/%{name}/tests
install -m 0644 tests/check_queue.c libcircle/queue.h %{buildroot}%{_datadir}/%{name}/tests/
cat > %{buildroot}%{_datadir}/%{name}/tests/run-original-tests.sh <<'SH'
#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
root=${1:-}
root=${root%%/}
fixtures="$root/usr/share/libcircle/tests"
(cd "$fixtures" && sha256sum -c SHA256SUMS)
scratch=$(mktemp -d)
trap 'rm -rf -- "$scratch"' EXIT
unset LD_LIBRARY_PATH CK_FORK
if test -n "$root"; then
    export LD_LIBRARY_PATH="$root/usr/lib64"
fi
# Keep Check's default fork isolation: every case initializes/finalizes MPI.
export CK_DEFAULT_TIMEOUT=120
read -r -a check_cflags <<< "$(pkg-config --cflags check)"
read -r -a check_libs <<< "$(pkg-config --libs check)"
printf '#include <libcircle.h>\n' > "$scratch/header.c"
mpicc -std=gnu99 -Wall -Wextra -Werror -I"$root/usr/include" -fsyntax-only "$scratch/header.c"
for opt in 0 2; do
    for linkage in shared static; do
        binary="$scratch/original-$linkage-O$opt"
        if test "$linkage" = shared; then
            libs=("$root/usr/lib64/libcircle.so")
        else
            libs=("$root/usr/lib64/libcircle.a")
        fi
        mpicc -std=gnu99 -O"$opt" -UNDEBUG -Wall -Wextra \
            -I"$root/usr/include" -I"$fixtures" "${check_cflags[@]}" \
            "$fixtures/check_queue.c" "${libs[@]}" "${check_libs[@]}" -o "$binary"
        if readelf -d "$binary" | grep -E '\((RPATH|RUNPATH)\)'; then
            echo 'FAIL unexpected embedded runtime path' >&2
            exit 1
        fi
        if test "$linkage" = shared; then
            readelf -d "$binary" | grep -F 'Shared library: [libcircle.so.2]'
            loaded=$(ldd "$binary" | awk '$1 == "libcircle.so.2" {print $3}')
            test -n "$loaded"
            test "$(readlink -f "$loaded")" = "$(readlink -f "$root/usr/lib64/libcircle.so.2.1.1")"
        elif readelf -d "$binary" | grep -F 'Shared library: [libcircle.'; then
            echo 'FAIL static replay linked shared libcircle' >&2
            exit 1
        fi
        timeout 600 "$binary" | tee "$scratch/$linkage-O$opt.log"
        grep -E '^100%: Checks: 4, Failures: 0, Errors: 0$' "$scratch/$linkage-O$opt.log"
        echo "PASS original-queue replay cases=4 linkage=$linkage opt=$opt scope=singleton-functional"
    done
done
SH
chmod 0755 %{buildroot}%{_datadir}/%{name}/tests/run-original-tests.sh
(cd %{buildroot}%{_datadir}/%{name}/tests && sha256sum check_queue.c queue.h run-original-tests.sh > SHA256SUMS)

%check
unset CK_FORK
export CK_DEFAULT_TIMEOUT=120
# Whole upstream suite, original assertions and default fork behavior retained.
# A generous QEMU timeout is still a failure, not a skipped test.
timeout 600 make -j1 check V=1
for expected in 'TOTAL: 1' 'PASS:  1' 'SKIP:  0' 'FAIL:  0' 'ERROR: 0'; do
    grep -F "$expected" tests/test-suite.log
done
grep -E '^100%: Checks: 4, Failures: 0, Errors: 0$' tests/check_queue.log
# Replays are not additional unique original cases.
bash %{buildroot}%{_datadir}/%{name}/tests/run-original-tests.sh %{buildroot}

%files
%license COPYING m4/lx_find_mpi.m4 m4/ltsugar.m4
%doc README.md AUTHORS
%{_libdir}/libcircle.so.2
%{_libdir}/libcircle.so.2.1.1

%files devel
%{_includedir}/libcircle.h
%{_libdir}/libcircle.so
%{_libdir}/libcircle.a
%{_libdir}/pkgconfig/libcircle.pc
%{_datadir}/%{name}/tests/

%changelog
* Fri Oct 16 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3-1
- Pin official v0.3 source, MPI dependencies and all original queue tests.
- Declare standard interfaces without changing any test body or assertion.
- Replay original cases against staged and installed shared/static libraries.
