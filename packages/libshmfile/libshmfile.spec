# SPDX-License-Identifier: Apache-2.0
%global upstream_commit 800c3d1bac0dd899c3d8737116db59334a828f31
Name:           libshmfile
Version:        1.1.0
Release:        1%{?dist}
Summary:        FILE stream interface for named shared-memory objects
License:        LGPL-2.1-only
URL:            https://github.com/kata198/shmfile
Source0:        libshmfile-1.1.0.tar.gz
Source1:        COPYING.GPL2
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  binutils
BuildRequires:  grep
BuildRequires:  sed
BuildRequires:  gzip
BuildRequires:  tar
BuildRequires:  rpm

%description
Small C library exposing named shared-memory objects through FILE streams
and file descriptors. The unversioned upstream shared library name is retained.
Validation is functional QEMU user-mode I/O, not native concurrency or security.

%package devel
Summary:        Header, static library and replay sources for libshmfile
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc
Requires:       glibc-devel
Requires:       bash
Requires:       coreutils
Requires:       grep
Provides:       %{name}-static = %{version}-%{release}

%description devel
Original header/static library and unchanged owner/guest example sources,
plus separately identified downstream sequential stream I/O checks.

%prep
%autosetup -n shmfile-%{upstream_commit}
cp -p %{SOURCE1} COPYING.GPL2
mkdir contract
cp -p examples/owner.c examples/guest.c examples/owner_guest_private.h contract/
cat > contract/check-stream.c <<'C'
/* SPDX-License-Identifier: Apache-2.0 */
/* Downstream functional I/O fixture, not a concurrent/native security test. */
#define _GNU_SOURCE
#include <shmfile.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#define CHECK(x) do { if (!(x)) { perror(#x); return 1; } } while (0)
int main(int argc, char **argv) {
    unsigned char a,b,c; const char *extra;
    FILE *owner,*guest; char data[6]={0};
    if (argc != 3) return 2;
    if (!strcmp(argv[1], "--destroy")) {
        CHECK(fshm_force_destroy(argv[2])==0);
        return 0;
    }
    if (strcmp(argv[1], "--check")) return 2;
    shmfile_get_version(&a,&b,&c,&extra);
    CHECK(a==1 && b==1 && c==0 && extra && !*extra);
    errno=0; CHECK(fshm_open(argv[2],0600,0)==NULL && errno==EINVAL);
    owner=fshm_create(argv[2],0600); CHECK(owner!=NULL);
    CHECK(fwrite("hello",1,5,owner)==5 && fflush(owner)==0);
    guest=fshm_guest_open(argv[2]); CHECK(guest!=NULL);
    CHECK(fread(data,1,5,guest)==5 && !strcmp(data,"hello"));
    CHECK(fseek(guest,0,SEEK_SET)==0);
    CHECK(fwrite("world",1,5,guest)==5 && fflush(guest)==0);
    CHECK(fseek(owner,0,SEEK_SET)==0);
    CHECK(fread(data,1,5,owner)==5 && !strcmp(data,"world"));
    CHECK(fileno(owner)>=0 && fileno(guest)>=0);
    CHECK(fclose(guest)==0 && fclose(owner)==0);
    errno=0; CHECK(fshm_guest_open(argv[2])==NULL && errno==ENOENT);
    puts("PASS downstream stream buffered-io=2 unlink=verified version=1.1.0");
    return 0;
}
C
cat > contract/run-tests.sh <<'SH'
#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail
test "$#" -le 1
root=${1:-/}
prefix="${root%%/}/usr"
self=$(cd -- "$(dirname -- "$0")" && pwd)
work=$(mktemp -d)
stream="/oe-shmfile-${work##*/}"
cleanup() {
    rc=$?
    if test -x "$work/check-shared" && test -e "/dev/shm/${stream#/}"; then
        "$work/check-shared" --destroy "$stream" || rc=1
    fi
    if test "$rc" -eq 0; then rm -rf -- "$work"; else echo "FAIL evidence retained: $work" >&2; fi
    exit "$rc"
}
trap cleanup EXIT
cd "$self"
sha256sum -c SHA256SUMS
export LD_LIBRARY_PATH="$prefix/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
for linkage in shared static; do
    if test "$linkage" = shared; then libs=(-L"$prefix/lib64" -lshmfile -lrt); else libs=("$prefix/lib64/libshmfile.a" -lrt); fi
    for app in owner guest; do
        gcc -std=gnu99 -O2 -g -UNDEBUG -I"$prefix/include" "$app.c" "${libs[@]}" -o "$work/$app-$linkage"
    done
    gcc -std=gnu99 -O2 -g -UNDEBUG -I"$prefix/include" check-stream.c "${libs[@]}" -o "$work/check-$linkage"
    "$work/check-$linkage" --check "$stream"
    # Original explicit zero-second argument, persistent mode: no sleep/poll race.
    "$work/owner-$linkage" "$stream" 0 > "$work/owner.log"
    grep -Fx 'shmfile version: 1.1.0' "$work/owner.log"
    "$work/guest-$linkage" "$stream" > "$work/guest1.log"
    grep -Fx 'Message is: Hello World!' "$work/guest1.log"
    grep -Fx 'Previous accesses: 0' "$work/guest1.log"
    "$work/guest-$linkage" "$stream" > "$work/guest2.log"
    grep -Fx 'Message is: Hello World!' "$work/guest2.log"
    grep -Fx 'Previous accesses: 1' "$work/guest2.log"
    "$work/check-$linkage" --destroy "$stream"
    if "$work/guest-$linkage" "$stream" > "$work/absent.log" 2>&1; then echo 'FAIL removed stream opened' >&2; exit 1; fi
    if "$work/owner-$linkage" x y z > "$work/invalid.log" 2>&1; then echo 'FAIL invalid owner arguments accepted' >&2; exit 1; fi
    echo "PASS upstream-example replay linkage=$linkage guests=2 negative-controls=2"
done
echo 'PASS downstream libshmfile shared-static=2 original-example-sources=unchanged'
SH
chmod 0755 contract/run-tests.sh
(cd contract && sha256sum owner.c guest.c owner_guest_private.h check-stream.c > SHA256SUMS)

%build
# Keep original default all, plus original static and examples targets.
make -j1 all static examples CFLAGS="%{optflags} -g -UNDEBUG" LDFLAGS="%{?build_ldflags}"

%install
make -j1 install install_static DESTDIR=%{buildroot} PREFIX=%{_prefix}
# Upstream only accepts PREFIX, so relocate its lib directory to target lib64.
install -d %{buildroot}%{_libdir}
mv %{buildroot}%{_prefix}/lib/libshmfile.so %{buildroot}%{_libdir}/libshmfile.so
mv %{buildroot}%{_prefix}/lib/libshmfile.a %{buildroot}%{_libdir}/libshmfile.a
chmod 0644 %{buildroot}%{_libdir}/libshmfile.so %{buildroot}%{_includedir}/shmfile.h
install -d %{buildroot}%{_datadir}/libshmfile/tests
cp -p contract/* %{buildroot}%{_datadir}/libshmfile/tests/

%check
# No registered upstream test/check target; retain original examples, not replacements.
examples/owner --version
examples/guest --version
bash %{buildroot}%{_datadir}/libshmfile/tests/run-tests.sh %{buildroot}

%files
%license LICENSE COPYING.GPL2
%doc README.md Changelog
%{_libdir}/libshmfile.so
%{_mandir}/man3/fshm_*.3*

%files devel
%{_includedir}/shmfile.h
%{_libdir}/libshmfile.a
%{_datadir}/libshmfile/

%changelog
* Fri Oct 16 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.0-1
- Pin official source, retain original builds/examples and complete license texts.
- Add separately identified staged/installed shared/static functional I/O replays.
