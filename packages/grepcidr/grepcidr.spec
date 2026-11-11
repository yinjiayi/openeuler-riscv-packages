# SPDX-License-Identifier: Apache-2.0
Name:           grepcidr
Version:        2.0
Release:        1%{?dist}
Summary:        Filter IPv4 and IPv6 addresses against CIDR patterns
License:        GPL-2.0-or-later AND Apache-2.0
URL:            https://pc-tools.net/unix/grepcidr/
Source0:        grepcidr-2.0.tar.gz
Source1:        Apache-2.0.txt
Patch0:         0001-define-IP-arithmetic-and-bounded-growth.patch
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  gzip
BuildRequires:  make
BuildRequires:  patch
BuildRequires:  sed
BuildRequires:  tar
Requires:       bash
Requires:       binutils
Requires:       coreutils
Requires:       diffutils
Requires:       findutils
Requires:       gawk
Requires:       grep

%description
Grepcidr filters IPv4 and IPv6 text against CIDR networks, single addresses
and IPv4 ranges. All original modes and default hint-scanning remain enabled
with narrow defined-arithmetic, growth and edge-input corrections. Strict
added CLI checks do not certify security, speed or native networking.

%prep
%setup -q -n grepcidr-2.0
find . -type f -print | LC_ALL=C sort > ../grepcidr-original-files.list
test "$(wc -l < ../grepcidr-original-files.list)" -eq 7
mkdir source-notices
while IFS= read -r item; do
    rel="${item#./}"
    destination="source-notices/$rel.notice"
    install -d "${destination%/*}"
    cp -p "$item" "$destination"
    chmod 0644 "$destination"
done < ../grepcidr-original-files.list
(cd source-notices; find . -type f -name '*.notice' -print | LC_ALL=C sort | while IFS= read -r item; do sha256sum "$item"; done) > ../grepcidr-original-SHA256SUMS
mv ../grepcidr-original-SHA256SUMS source-notices/SHA256SUMS
test "$(wc -l < source-notices/SHA256SUMS)" -eq 7
%autopatch -p1
cp -p %{SOURCE1} Apache-2.0.txt
cat > run-regressions.sh <<'REGRESSION_SCRIPT'
#!/usr/bin/bash
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 openEuler RISC-V package contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy at https://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License. Full text ships with this package.
set -euo pipefail
export LC_ALL=C LANG=C PATH=/usr/bin:/bin
unset LD_LIBRARY_PATH LD_PRELOAD
test "$#" -eq 3
binary=$(readlink -f -- "$1")
expected=$(readlink -f -- "$2")
version_file=$(readlink -f -- "$3")
test -x "$binary" && test "$binary" -ef "$expected"
work=$(mktemp -d /tmp/grepcidr-regression.XXXXXXXX)
finish() {
    status=$?
    trap - EXIT
    set +e
    printf 'GREPCIDR_QA_WORK %%s\n' "$work"
    for raw in "$work"/*; do
        test -f "$raw" || continue
        printf '\nGREPCIDR_RAW_BEGIN %%s\n' "${raw##*/}" || status=1
        sha256sum "$raw" || status=1
        cat "$raw" || status=1
        printf '\nGREPCIDR_RAW_END %%s\n' "${raw##*/}" || status=1
    done
    printf 'GREPCIDR_QA_EXIT %%s\n' "$status"
    exit "$status"
}
trap finish EXIT
sha256sum "$binary" > "$work/binary-before.sha256"
: > "$work/empty"
invoke() {
    local label=$1 wanted_status=$2 input=$3 wanted_out=$4 wanted_err=$5
    shift 5
    local status=0
    "$binary" "$@" < "$input" > "$work/$label.stdout" 2> "$work/$label.stderr" || status=$?
    printf '%%s\n' "$status" > "$work/$label.status"
    test "$status" -eq "$wanted_status"
    cmp "$wanted_out" "$work/$label.stdout"
    cmp "$wanted_err" "$work/$label.stderr"
}

# The original -V intentionally returns EXIT_ERROR(2); preserve that contract.
invoke version 2 "$work/empty" "$version_file" "$work/empty" -V
printf 'grepcidr case01 version-exit2: PASS\n'

printf '0.0.0.0\n127.255.255.255\n128.0.0.0\n192.0.2.0\n192.0.2.1\n192.0.2.255\n198.51.100.1\n255.255.255.255\n' > "$work/v4.input"
printf '128.0.0.0\n192.0.2.0\n192.0.2.1\n192.0.2.255\n198.51.100.1\n255.255.255.255\n' > "$work/v4-half.expected"
printf '192.0.2.0\n192.0.2.1\n192.0.2.255\n' > "$work/v4-subnet.expected"
printf '255.255.255.255\n' > "$work/v4-host.expected"
invoke v4-zero 0 "$work/v4.input" "$work/v4.input" "$work/empty" 0.0.0.0/0
invoke v4-one 0 "$work/v4.input" "$work/v4-half.expected" "$work/empty" 128.0.0.0/1
invoke v4-twentyfour 0 "$work/v4.input" "$work/v4-subnet.expected" "$work/empty" 192.0.2.0/24
invoke v4-thirtytwo 0 "$work/v4.input" "$work/v4-host.expected" "$work/empty" 255.255.255.255/32
printf 'grepcidr case02 v4-unsigned-boundaries: PASS\n'

printf '::\n::1\n2001:db8::1\n2001:db8:ffff::ffff\n2001:db9::1\n8000::1\nffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff\n' > "$work/v6.input"
printf '2001:db8::1\n2001:db8:ffff::ffff\n' > "$work/v6-network.expected"
printf 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff\n' > "$work/v6-host.expected"
invoke v6-zero 0 "$work/v6.input" "$work/v6.input" "$work/empty" ::/0
invoke v6-thirtytwo 0 "$work/v6.input" "$work/v6-network.expected" "$work/empty" 2001:db8::/32
invoke v6-full 0 "$work/v6.input" "$work/v6-host.expected" "$work/empty" ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff/128
printf 'grepcidr case03 v6-boundaries: PASS\n'

printf '# fixture\n\n192.0.2.0/25\n192.0.2.64/26\n2001:db8::/32\n' > "$work/mixed.patterns"
printf 'lead 192.0.2.1 end\n192.0.2.2 end\nreverse 1.2.0.192.example\nno address\nv6 2001:db8::1 end\n198.51.100.7 end\n' > "$work/mixed.input"
printf 'lead 192.0.2.1 end\n192.0.2.2 end\nv6 2001:db8::1 end\n' > "$work/mixed.expected"
printf '192.0.2.2 end\n' > "$work/strict.expected"
printf '198.51.100.7 end\n' > "$work/invert.expected"
printf 'reverse 1.2.0.192.example\nno address\n198.51.100.7 end\n' > "$work/include.expected"
printf '3\n' > "$work/count.expected"
invoke mixed 0 "$work/mixed.input" "$work/mixed.expected" "$work/empty" -f "$work/mixed.patterns"
invoke strict 0 "$work/mixed.input" "$work/strict.expected" "$work/empty" -x -f "$work/mixed.patterns"
invoke inverse 0 "$work/mixed.input" "$work/invert.expected" "$work/empty" -v -f "$work/mixed.patterns"
invoke include 0 "$work/mixed.input" "$work/include.expected" "$work/empty" -i -f "$work/mixed.patterns"
invoke count 0 "$work/mixed.input" "$work/count.expected" "$work/empty" -c -f "$work/mixed.patterns"
printf 'grepcidr case04 patterns-hints-modes: PASS\n'

# One more than INIT_NETWORKS in each independent array exercises both growth paths.
gawk 'BEGIN {for(i=0;i<8193;i++)print "192.0.2.1"; for(i=0;i<8193;i++)print "2001:db8::1"}' > "$work/growth.patterns"
test "$(wc -l < "$work/growth.patterns")" -eq 16386
printf '192.0.2.1\n192.0.2.2\n2001:db8::1\n2001:db8::2\n' > "$work/growth.input"
printf '192.0.2.1\n2001:db8::1\n' > "$work/growth.expected"
invoke growth 0 "$work/growth.input" "$work/growth.expected" "$work/empty" -f "$work/growth.patterns"
printf 'grepcidr case05 both-array-growth: PASS\n'

for length in 511 1023; do
    gawk -v n="$length" 'BEGIN {for(i=0;i<n-10;i++)printf "x"; printf " 192.0.2.1"}' > "$work/eof-$length.input"
    test "$(wc -c < "$work/eof-$length.input")" -eq "$length"
    invoke "eof-$length" 0 "$work/eof-$length.input" "$work/eof-$length.input" "$work/empty" 192.0.2.0/24
done
gawk 'BEGIN {for(i=0;i<4096;i++)printf "x"; print " 192.0.2.1"}' > "$work/long.input"
invoke long-line 0 "$work/long.input" "$work/long.input" "$work/empty" 192.0.2.0/24
printf '\303\251 high-byte 192.0.2.1\n' > "$work/highbyte.input"
invoke high-byte 0 "$work/highbyte.input" "$work/highbyte.input" "$work/empty" 192.0.2.0/24
invoke no-match 1 "$work/v4.input" "$work/empty" "$work/empty" 203.0.113.0/24
invoke empty-input 1 "$work/empty" "$work/empty" "$work/empty" 192.0.2.0/24
printf 'grepcidr: Not a valid pattern: 192.0.2.1/24\n' > "$work/bad-align.expected"
invoke bad-align 1 "$work/empty" "$work/empty" "$work/bad-align.expected" -s 192.0.2.1/24
missing="$work/nonexistent-input"
printf 'grepcidr: %%s: No such file or directory\n' "$missing" > "$work/missing.expected"
invoke missing-file 2 "$work/empty" "$work/empty" "$work/missing.expected" 192.0.2.0/24 "$missing"
printf 'grepcidr case06 EOF-highbyte-and-exit-boundaries: PASS\n'
sha256sum "$binary" > "$work/binary-after.sha256"
cmp "$work/binary-before.sha256" "$work/binary-after.sha256"
printf 'grepcidr strict CLI: 6 groups PASS\n'
REGRESSION_SCRIPT
cat > expected-version.txt <<'EXPECTED_VERSION'
grepcidr 2.0
Copyright (C) 2004 - 2014  Jem E. Berkes <jem@berkes.ca>

EXPECTED_VERSION

%build
%set_build_flags
# Preserve upstream's effective optimization/warning defaults, not -Wno-error.
%make_build CC=gcc CPPFLAGS="$CPPFLAGS" CFLAGS="$CFLAGS -O3 -Wall -Werror" LDFLAGS="$LDFLAGS"

%install
%make_install PREFIX=%{_prefix}
install -Dpm 0755 run-regressions.sh %{buildroot}%{_libexecdir}/grepcidr/run-regressions.sh
install -Dpm 0644 expected-version.txt %{buildroot}%{_datadir}/grepcidr-tests/expected-version.txt
install -d %{buildroot}%{_licensedir}/%{name}
cp -a source-notices %{buildroot}%{_licensedir}/%{name}/source-notices
install -pm 0644 COPYING Apache-2.0.txt %{buildroot}%{_licensedir}/%{name}/

%check
set -eu
# Original2.0 has no check/test target or registered test programs; do not
# invent a successful make check. Original all/install/suppliedman stay intact.
printf 'grepcidr upstream suite: no check/test target in original2.0; added CLI QA follows.\n'
bash ./run-regressions.sh "$PWD/grepcidr" "$PWD/grepcidr" "$PWD/expected-version.txt" > strict-cli.stdout 2> strict-cli.stderr || { status=$?; cat strict-cli.stdout strict-cli.stderr; exit "$status"; }
cat strict-cli.stdout strict-cli.stderr
test ! -s strict-cli.stderr
gawk '/^grepcidr case0[1-6] .*: PASS$/{n++} END{exit(n!=6)}' strict-cli.stdout
test "$(grep -c '^grepcidr strict CLI: 6 groups PASS$' strict-cli.stdout)" -eq 1
# Install-post stripping precedes check: bind final installed payload bytes.
(cd %{buildroot}; sha256sum ./usr/bin/grepcidr ./usr/libexec/grepcidr/run-regressions.sh ./usr/share/grepcidr-tests/expected-version.txt) > %{buildroot}%{_datadir}/grepcidr-tests/SHA256SUMS

%files
%license %{_licensedir}/%{name}
%doc README ChangeLog grepcidr.sgml
%{_bindir}/grepcidr
%{_mandir}/man1/grepcidr.1*
%{_libexecdir}/grepcidr
%{_datadir}/grepcidr-tests

%changelog
* Tue Oct 27 2026 openEuler RISC-V package contributors - 2.0-1
- Preserve original all/install/man and modes with narrow source edge fixes.
- Add six strict numeric CLI regression groups; preserve original version exit2.
