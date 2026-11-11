# SPDX-License-Identifier: Apache-2.0
Name:           libblip-buf
Version:        1.1.1
Release:        2%{?dist}
Summary:        Band-limited audio waveform synthesis library
License:        LGPL-2.1-or-later
URL:            https://gitlab.com/TASVideos/libblip_buf
Source0:        libblip_buf-1.1.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  binutils
BuildRequires:  glibc-devel
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  grep
BuildRequires:  gawk
BuildRequires:  sed
BuildRequires:  bash
BuildRequires:  tar
BuildRequires:  gzip
Requires:       bash
Requires:       binutils
Requires:       coreutils
Requires:       grep
Requires:       gawk
Requires:       diffutils

%description
Band-limited audio waveform synthesis library for sound-chip emulation.
The original default shared-library and compatibility-filename targets are
retained; the compatibility filename is a Linux ELF, not a Windows DLL.
The complete corresponding source is retained in the source RPM.

%prep
%setup -q -n libblip_buf-8f5101b1d3229657ce71c2d395e78c8ad69f2cb1
# Preserve all eight original files byte-for-byte, including historical docs
# and makefile_orig, before generating any downstream QA source.
mkdir source-notices
for original in Makefile blip_buf.c blip_buf.h blip_buf.txt changes.txt license.txt makefile_orig readme.txt; do
    cp -p "$original" "source-notices/$original.notice"
done
(cd source-notices && sha256sum *.notice > SHA256SUMS)
cat > api-smoke.c <<'BLIP_API_EOF'
/* SPDX-License-Identifier: LGPL-2.1-or-later
 * Copyright (C) 2026 openEuler RISC-V packaging contributors.
 * You may redistribute and modify this QA under the GNU Lesser General
 * Public License version 2.1 or, at your option, any later version.
 * Distributed WITHOUT ANY WARRANTY, including MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE. See the accompanying full license.txt.
 * Downstream bounded contract checks, not upstream tests or audio-quality QA.
 */
#include <blip_buf.h>
#include <stdio.h>
#include <stdlib.h>
#define CHECK(e) do { if (!(e)) { fputs("failed: " #e "\n", stderr); return 1; } } while (0)
int main(void) {
    blip_t *m = blip_new(128);
    short out[129];
    int i, nonzero;
    CHECK(m != NULL);
    CHECK(blip_samples_avail(m) == 0);
    CHECK(blip_clocks_needed(m, 0) == 0);
    CHECK(blip_read_samples(m, out, 0, 0) == 0);
    blip_delete(NULL);
    puts("PASS allocation-default-zero");

    blip_set_rates(m, 16.0, 1.0);
    blip_clear(m);
    CHECK(blip_clocks_needed(m, 16) == 256);
    blip_end_frame(m, 256);
    CHECK(blip_samples_avail(m) == 16);
    blip_clear(m);
    CHECK(blip_samples_avail(m) == 0);
    puts("PASS rates-frame-clear");

    for (i = 0; i < 129; ++i) out[i] = 22222;
    blip_end_frame(m, 1024);
    CHECK(blip_samples_avail(m) == 64);
    CHECK(blip_read_samples(m, out, 7, 0) == 7);
    CHECK(blip_samples_avail(m) == 57);
    CHECK(blip_read_samples(m, out + 7, 100, 0) == 57);
    CHECK(blip_samples_avail(m) == 0);
    for (i = 0; i < 64; ++i) CHECK(out[i] == 0);
    CHECK(out[64] == 22222);
    puts("PASS mono-silence-partial-read");

    blip_clear(m);
    for (i = 0; i < 129; ++i) out[i] = 22222;
    blip_end_frame(m, 128);
    CHECK(blip_read_samples(m, out, 8, 1) == 8);
    for (i = 0; i < 8; ++i) { CHECK(out[2*i] == 0); CHECK(out[2*i+1] == 22222); }
    CHECK(out[16] == 22222);
    puts("PASS stereo-stride-sentinel");

    blip_clear(m);
    blip_add_delta(m, 0, 1000);
    blip_add_delta(m, 512, -1000);
    blip_end_frame(m, 1024);
    CHECK(blip_read_samples(m, out, 64, 0) == 64);
    nonzero = 0;
    for (i = 0; i < 64; ++i) nonzero += out[i] != 0;
    CHECK(nonzero > 0);
    puts("PASS sinc-delta-nonzero");

    blip_clear(m);
    blip_add_delta_fast(m, 0, 1000);
    blip_add_delta_fast(m, 512, -1000);
    blip_end_frame(m, 1024);
    CHECK(blip_read_samples(m, out, 64, 0) == 64);
    nonzero = 0;
    for (i = 0; i < 64; ++i) nonzero += out[i] != 0;
    CHECK(nonzero > 0);
    blip_delete(m);
    puts("PASS fast-delta-nonzero");
    return 0;
}
BLIP_API_EOF
cat > run-qa.sh <<'BLIP_QA_EOF'
#!/usr/bin/env bash
# SPDX-License-Identifier: LGPL-2.1-or-later
# Copyright (C) 2026 openEuler RISC-V packaging contributors.
# Redistributable/modifiable under LGPL2.1-or-later; no warranty.
# Full LGPL2.1 is supplied in license.txt with the library.
set -euo pipefail
prefix=${1-}
case "$prefix" in ''|/*) ;; *) exit 2;; esac
libdir="$prefix/usr/lib64"
program="$prefix/usr/libexec/libblip-buf/api-smoke"
data="$prefix/usr/share/libblip-buf-tests"
test "$libdir/libblip_buf.so.1" -ef "$libdir/libblip_buf.so.1.1.1"
(cd "${prefix}/" && sha256sum -c "$data/SHA256SUMS")
work=$(mktemp -d /tmp/libblip-buf-qa.XXXXXXXX)
trap 'rm -r -- "$work"' EXIT
expected='PASS allocation-default-zero
PASS rates-frame-clear
PASS mono-silence-partial-read
PASS stereo-stride-sentinel
PASS sinc-delta-nonzero
PASS fast-delta-nonzero'
printf '%%s\n' "$expected" > "$work/expected"
normal_status=0
env -u LD_PRELOAD -u LD_AUDIT -u LD_DEBUG_OUTPUT -u LD_DEBUG \
    LD_LIBRARY_PATH="$libdir" "$program" > "$work/normal" 2> "$work/normal-error" || normal_status=$?
cat "$work/normal" "$work/normal-error"
test "$normal_status" -eq 0
test ! -s "$work/normal-error"
cmp "$work/normal" "$work/expected"
debug_status=0
env -u LD_PRELOAD -u LD_AUDIT -u LD_DEBUG_OUTPUT \
    LD_LIBRARY_PATH="$libdir" LD_BIND_NOW=1 LD_DEBUG=bindings \
    "$program" > "$work/results" 2> "$work/bindings" || debug_status=$?
# Retain the complete raw streams even when the program or binding check fails.
cat "$work/results" "$work/bindings"
sha256sum "$program" "$libdir/libblip_buf.so.1.1.1"
test "$debug_status" -eq 0
cmp "$work/results" "$work/expected"
gawk -v program="$program" '
BEGIN {
 n=split("blip_new blip_delete blip_set_rates blip_clear blip_add_delta blip_add_delta_fast blip_clocks_needed blip_end_frame blip_samples_avail blip_read_samples",a," ")
 for(i=1;i<=n;i++) needed[a[i]]=1
}
{
 line=$0; gsub(/[[:space:]]+/," ",line)
 sym=$NF; gsub(/[^[:alnum:]_]/,"",sym)
 if(index(line,"binding file " program " [0]") && (sym in needed)) {
  rest=line; sub(/^.*binding file /,"",rest)
  i=index(rest," [0] to "); if(!i) exit 1
  caller=substr(rest,1,i-1); rest=substr(rest,i+8)
  j=index(rest," [0]: normal symbol "); if(!j) exit 1
  target=substr(rest,1,j-1)
  print caller "\t" target "\t" sym
  seen[sym]=1
 }
}
END { for(s in needed) if(!(s in seen)) exit 1 }
' "$work/bindings" > "$work/binding-paths"
while IFS=$'\t' read -r caller target symbol; do
    test "$caller" -ef "$program"
    test "$target" -ef "$libdir/libblip_buf.so.1.1.1"
    echo "PASS same-file binding $symbol"
done < "$work/binding-paths"
echo 'PASS exact-installed-library-bindings-10'
BLIP_QA_EOF

%build
# Both original default targets (dll and so) remain selected. PIC, hardening,
# and an explicit Linux SONAME are command-line flags, not a source patch.
%make_build CC=gcc CFLAGS="%{optflags} -fPIC -UNDEBUG" LFLAGS="-shared %{?build_ldflags} -Wl,-soname,libblip_buf.so.1"

%install
install -D -m 0755 libblip_buf.so.1.1.1 %{buildroot}%{_libdir}/libblip_buf.so.1.1.1
ln -s libblip_buf.so.1.1.1 %{buildroot}%{_libdir}/libblip_buf.so.1
ln -s libblip_buf.so.1 %{buildroot}%{_libdir}/libblip_buf.so
install -D -m 0755 blip_buf.dll %{buildroot}%{_libdir}/libblip-buf/blip_buf.dll
install -D -m 0644 blip_buf.h %{buildroot}%{_includedir}/blip_buf.h
install -D -m 0644 api-smoke.c %{buildroot}%{_datadir}/libblip-buf-tests/api-smoke.c
install -m 0644 run-qa.sh %{buildroot}%{_datadir}/libblip-buf-tests/run-qa.sh
mkdir -p %{buildroot}%{_libexecdir}/libblip-buf
# Prove the source include view equals the staged installed header, without
# embedding an absolute BUILDROOT include directory in driver debug records.
cmp blip_buf.h %{buildroot}%{_includedir}/blip_buf.h
gcc %{optflags} -std=c99 -I. api-smoke.c \
    -L%{buildroot}%{_libdir} %{?build_ldflags} -Wl,-z,now -lblip_buf \
    -o %{buildroot}%{_libexecdir}/libblip-buf/api-smoke

%check
# Actual formal-release Makefile has no check/test target; the historical
# makefile_orig references tests absent from BOTH offered source archives.
# Do not execute that non-default incomplete recipe or claim upstream QA passed.
for binary in libblip_buf.so.1.1.1 blip_buf.dll %{buildroot}%{_libexecdir}/libblip-buf/api-smoke; do
    readelf -h "$binary" | grep 'Class:.*ELF64'
    readelf -h "$binary" | grep 'Machine:.*RISC-V'
done
readelf -d libblip_buf.so.1.1.1 | grep 'SONAME.*libblip_buf.so.1'
readelf -d %{buildroot}%{_libexecdir}/libblip-buf/api-smoke | grep 'NEEDED.*libblip_buf.so.1'
(cd source-notices && sha256sum -c SHA256SUMS)
# RPM's install-post brp/debug processing precedes check: bind actual final
# driver/shared/compatibility bytes, not a pre-strip executable checksum.
(cd %{buildroot} && sha256sum usr/libexec/libblip-buf/api-smoke usr/lib64/libblip_buf.so.1.1.1 usr/lib64/libblip-buf/blip_buf.dll usr/share/libblip-buf-tests/api-smoke.c usr/share/libblip-buf-tests/run-qa.sh > usr/share/libblip-buf-tests/SHA256SUMS)
bash run-qa.sh "%{buildroot}"

%files
%license license.txt source-notices
%doc readme.txt blip_buf.txt changes.txt
%{_libdir}/libblip_buf.so.1.1.1
%{_libdir}/libblip_buf.so.1
%{_libdir}/libblip_buf.so
%dir %{_libdir}/libblip-buf
%{_libdir}/libblip-buf/blip_buf.dll
%{_includedir}/blip_buf.h
%dir %{_libexecdir}/libblip-buf
%{_libexecdir}/libblip-buf/api-smoke
%dir %{_datadir}/libblip-buf-tests
%{_datadir}/libblip-buf-tests/api-smoke.c
%{_datadir}/libblip-buf-tests/run-qa.sh
%{_datadir}/libblip-buf-tests/SHA256SUMS

%changelog
* Mon Oct 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.1-2
- Compare staged header bytes before compiling the QA driver with a source include view.
- Keep debuginfo, check-buildroot, original outputs and all build/install QA enabled.

* Mon Oct 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.1-1
- Package exact official release; retain both default outputs and all source notices.
- Add installed-header API and strict same-file loader checks; no native/audio-quality claim.
