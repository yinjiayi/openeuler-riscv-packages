# SPDX-License-Identifier: Apache-2.0
Name:           liburlmatch
Version:        1.0
Release:        1%{?dist}
Summary:        Static URL wildcard matching development library
License:        AGPL-3.0-only
URL:            https://github.com/clbr/urlmatch
%global upstream_commit 24f72a0ea15402d28143fc84ca60b13f3dd033a7
Source0:        liburlmatch-1.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  binutils
BuildRequires:  rpm
BuildRequires:  gzip
BuildRequires:  tar
BuildRequires:  grep
BuildRequires:  gawk
BuildRequires:  sed
BuildRequires:  findutils
BuildRequires:  diffutils
BuildRequires:  zlib-devel
Provides:       liburlmatch-devel = %{version}-%{release}
Provides:       liburlmatch-static = %{version}-%{release}
Requires:       gcc
Requires:       zlib-devel
Requires:       bash
Requires:       coreutils
Requires:       binutils
Requires:       rpm

%description
URL wildcard matching library with simple, optimized and rated interfaces.
Upstream builds a static archive only. This development package includes the
public header, static archive and unchanged original test sources for installed
contract verification; it does not introduce a shared-library ABI.

%prep
%autosetup -n urlmatch-%{upstream_commit}
mkdir -p contract/upstream/test
cp -p internal.h lrtypes.h contract/upstream/
cp -p test/*.c test/test.h test/Makefile test/run-tests.sh contract/upstream/test/
(cd contract/upstream && sha256sum internal.h lrtypes.h test/*.c test/test.h test/Makefile test/run-tests.sh) > contract/SHA256SUMS
cat > contract/run-original-tests.sh <<'SH'
#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
test "$#" -le 1
root=${1:-/}
self=$(cd -- "$(dirname -- "$0")" && pwd)
work=$(mktemp -d)
finish() {
    rc=$?
    if test "$rc" -eq 0; then rm -rf -- "$work"; else printf 'original test evidence retained: %s\n' "$work" >&2; fi
    exit "$rc"
}
trap finish EXIT
programs=(allocfree bin count opti rated shortrule simple str)
cd "$self/upstream"
sha256sum -c ../SHA256SUMS
for source in test/*.c; do basename "$source" .c; done | LC_ALL=C sort > "$work/observed"
printf '%s\n' "${programs[@]}" > "$work/expected"
cmp "$work/expected" "$work/observed"
test -s "${root%/}/usr/include/urlmatch.h"
test -s "${root%/}/usr/lib64/liburlmatch.a"
for name in "${programs[@]}"; do
    gcc -O2 -g -UNDEBUG -Wall -Wextra \
        -I"${root%/}/usr/include" -I"$self/upstream" -I"$self/upstream/test" \
        "$self/upstream/test/$name.c" "${root%/}/usr/lib64/liburlmatch.a" -lz -o "$work/$name"
done
cd "$work"
for name in "${programs[@]}"; do
    test -x "$work/$name"
    "$work/$name"
    printf 'PASS installed original test: %s\n' "$name"
done
printf 'PASS installed original programs=8 skips=0 source=unchanged\n'
SH

%build
# Environment assignments retain upstream's appended warning flags.
export CC=gcc
export CFLAGS="%{optflags} -g -UNDEBUG"
export LDFLAGS="%{?build_ldflags}"
%make_build

%install
%make_install PREFIX=%{_prefix}
# The upstream static-only installer uses PREFIX/lib on every architecture.
install -d %{buildroot}%{_libdir}
if test "%{_libdir}" != "%{_prefix}/lib"; then
    mv %{buildroot}%{_prefix}/lib/liburlmatch.a %{buildroot}%{_libdir}/liburlmatch.a
fi
install -d %{buildroot}%{_datadir}/liburlmatch/tests
cp -pr contract/upstream %{buildroot}%{_datadir}/liburlmatch/tests/
install -m 0644 contract/SHA256SUMS %{buildroot}%{_datadir}/liburlmatch/tests/
install -m 0755 contract/run-original-tests.sh %{buildroot}%{_datadir}/liburlmatch/tests/
cmp urlmatch.h %{buildroot}%{_includedir}/urlmatch.h

%check
export CC=gcc
export CFLAGS="%{optflags} -g -UNDEBUG"
export LDFLAGS="%{?build_ldflags}"
# Retain the default test target. A trailing zlib avoids --as-needed link order.
make -j1 test LDLIBS=-lz
# Upstream's runner prints failures but does not propagate a failing exit code.
# Check membership and direct exit codes without editing or omitting any test.
for source in test/*.c; do basename "$source" .c; done | LC_ALL=C sort > contract/observed
printf '%s\n' allocfree bin count opti rated shortrule simple str > contract/expected
cmp contract/expected contract/observed
for name in allocfree bin count opti rated shortrule simple str; do
    test -x "test/$name"
    (cd test && "./$name")
    printf 'PASS default original test: %s\n' "$name"
done
bash %{buildroot}%{_datadir}/liburlmatch/tests/run-original-tests.sh %{buildroot}

%files
%license COPYING
%doc README.asciidoc
%{_includedir}/urlmatch.h
%{_libdir}/liburlmatch.a
%{_datadir}/liburlmatch/

%changelog
* Fri Oct 16 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0-1
- Package the original static-only default build without source patches.
- Retain all eight original tests and verify installed static/header contracts.
