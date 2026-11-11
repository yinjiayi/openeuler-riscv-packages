# SPDX-License-Identifier: Apache-2.0
Name:           sipcalc
Version:        1.1.6
Release:        1%{?dist}
Summary:        Console IPv4 and IPv6 subnet calculator
License:        BSD-3-Clause AND FSFUL AND FSFULLR AND X11 AND GPL-3.0-or-later WITH Autoconf-exception-generic AND LicenseRef-Public-Domain AND Apache-2.0
URL:            https://routemeister.net/projects/sipcalc/
Source0:        sipcalc-1.1.6.tar.gz
Source1:        GPL-3.0.txt
Source2:        Apache-2.0.txt
Patch0:         0001-fix-empty-line-and-explicit-ipv6.patch
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
Sipcalc displays IPv4/IPv6 addresses, masks, prefixes and subnet ranges.
The original interface and DNS-resolution features, CLI options and manual
remain enabled. Added deterministic numeric-address checks are not a
network, interface portability, performance or security certification.

%prep
%setup -q -n sipcalc-1.1.6
find . -type f -print | LC_ALL=C sort > ../sipcalc-original-files.list
test "$(wc -l < ../sipcalc-original-files.list)" -eq 32
mkdir source-notices
while IFS= read -r item; do
    rel="${item#./}"
    destination="source-notices/$rel.notice"
    install -d "${destination%/*}"
    cp -p "$item" "$destination"
    chmod 0644 "$destination"
done < ../sipcalc-original-files.list
(cd source-notices; find . -type f -name '*.notice' -print | LC_ALL=C sort | while IFS= read -r item; do sha256sum "$item"; done) > ../sipcalc-original-SHA256SUMS
mv ../sipcalc-original-SHA256SUMS source-notices/SHA256SUMS
test "$(wc -l < source-notices/SHA256SUMS)" -eq 32
%autopatch -p1
cp -p %{SOURCE1} GPL-3.0.txt
cp -p %{SOURCE2} Apache-2.0.txt
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
# limitations under the License. The full text is installed with the package.
set -euo pipefail
export LC_ALL=C LANG=C
export PATH=/usr/bin:/bin
test "$#" -eq 3
binary=$(readlink -f -- "$1")
expected=$(readlink -f -- "$2")
version_file=$3
test -x "$binary" && test "$binary" -ef "$expected"
work=$(mktemp -d /tmp/sipcalc-regression.XXXXXXXX)
finish() {
    status=$?
    trap - EXIT
    set +e
    printf 'SIPCALC_QA_WORK %%s\n' "$work"
    for raw in "$work"/*; do
        test -f "$raw" || continue
        printf '\nSIPCALC_RAW_BEGIN %%s\n' "${raw##*/}" || status=1
        sha256sum "$raw" || status=1
        cat "$raw" || status=1
        printf '\nSIPCALC_RAW_END %%s\n' "${raw##*/}" || status=1
    done
    printf 'SIPCALC_QA_EXIT %%s\n' "$status"
    exit "$status"
}
trap finish EXIT
sha256sum "$binary" > "$work/binary-before.sha256"
run_case() {
    local label=$1 expected_status=$2
    shift 2
    local status=0
    "$binary" "$@" > "$work/$label.stdout" 2> "$work/$label.stderr" || status=$?
    printf '%%s\n' "$status" > "$work/$label.status"
    test "$status" -eq "$expected_status"
    test ! -s "$work/$label.stderr"
}
expect_v4() {
    local destination=$1 command_text=$2
    printf -- '-[ipv4 : %%s] - 0\n\n' "$command_text" > "$destination"
    cat >> "$destination" <<'V4'
[CIDR]
Host address		- 192.0.2.129
Host address (decimal)	- 3221226113
Host address (hex)	- C0000281
Network address		- 192.0.2.128
Network mask		- 255.255.255.128
Network mask (bits)	- 25
Network mask (hex)	- FFFFFF80
Broadcast address	- 192.0.2.255
Cisco wildcard		- 0.0.0.127
Addresses in network	- 128
Network range		- 192.0.2.128 - 192.0.2.255
Usable range		- 192.0.2.129 - 192.0.2.254

-
V4
}
expect_v6() {
    local destination=$1
    cat > "$destination" <<'V6'
-[ipv6 : 2001:db8:1::1234/64] - 0

[IPV6 INFO]
Expanded Address	- 2001:0db8:0001:0000:0000:0000:0000:1234
Compressed address	- 2001:db8:1::1234
Subnet prefix (masked)	- 2001:db8:1:0:0:0:0:0/64
Address ID (masked)	- 0:0:0:0:0:0:0:1234/64
Prefix address		- ffff:ffff:ffff:ffff:0:0:0:0
Prefix length		- 64
Address type		- Aggregatable Global Unicast Addresses
Network range		- 2001:0db8:0001:0000:0000:0000:0000:0000 -
			  2001:0db8:0001:0000:ffff:ffff:ffff:ffff

-
V6
}
run_case case01-version 0 -v
cmp "$version_file" "$work/case01-version.stdout"
printf 'sipcalc case01 version: PASS\n'

expect_v4 "$work/case02.expected" '192.0.2.129/25'
run_case case02-v4 0 192.0.2.129/25
cmp "$work/case02.expected" "$work/case02-v4.stdout"
cat > "$work/case02-host.expected" <<'HOST'
-[ipv4 : 192.0.2.129/32] - 0

[CIDR]
Host address		- 192.0.2.129
Host address (decimal)	- 3221226113
Host address (hex)	- C0000281
Network address		- 192.0.2.129
Network mask		- 255.255.255.255
Network mask (bits)	- 32
Network mask (hex)	- FFFFFFFF
Broadcast address	- 192.0.2.129
Cisco wildcard		- 0.0.0.0
Addresses in network	- 1
Network range		- 192.0.2.129 - 192.0.2.129

-
HOST
run_case case02-host 0 192.0.2.129/32
cmp "$work/case02-host.expected" "$work/case02-host.stdout"
printf 'sipcalc case02 IPv4 CIDR/range: PASS\n'

expect_v4 "$work/case03-dotted.expected" '192.0.2.129 255.255.255.128'
run_case case03-dotted 0 192.0.2.129 255.255.255.128
cmp "$work/case03-dotted.expected" "$work/case03-dotted.stdout"
expect_v4 "$work/case03-hex.expected" '192.0.2.129 0xffffff80'
run_case case03-hex 0 192.0.2.129 0xffffff80
cmp "$work/case03-hex.expected" "$work/case03-hex.stdout"
printf 'sipcalc case03 dotted/hex netmask equivalence: PASS\n'

expect_v6 "$work/case04.expected"
run_case case04-v6 0 2001:db8:1::1234/64
cmp "$work/case04.expected" "$work/case04-v6.stdout"
run_case case04-explicit-v6 0 -6 2001:db8:1::1234/64
cmp "$work/case04.expected" "$work/case04-explicit-v6.stdout"
cat > "$work/case04-host.expected" <<'HOST6'
-[ipv6 : 2001:db8:1::1234/128] - 0

[IPV6 INFO]
Expanded Address	- 2001:0db8:0001:0000:0000:0000:0000:1234
Compressed address	- 2001:db8:1::1234
Subnet prefix (masked)	- 2001:db8:1:0:0:0:0:1234/128
Address ID (masked)	- 0:0:0:0:0:0:0:0/128
Prefix address		- ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff
Prefix length		- 128
Address type		- Aggregatable Global Unicast Addresses
Network range		- 2001:0db8:0001:0000:0000:0000:0000:1234 -
			  2001:0db8:0001:0000:0000:0000:0000:1234

-
HOST6
run_case case04-host 0 2001:db8:1::1234/128
cmp "$work/case04-host.expected" "$work/case04-host.stdout"
printf 'sipcalc case04 IPv6 compressed/explicit/range: PASS\n'

cat > "$work/case05.input" <<'INPUT'

# ignored comment
192.0.2.129/25

2001:db8:1::1234/64
# final comment
INPUT
cat "$work/case02.expected" "$work/case04.expected" > "$work/case05.expected"
status=0
"$binary" - < "$work/case05.input" > "$work/case05-stdin.stdout" 2> "$work/case05-stdin.stderr" || status=$?
printf '%%s\n' "$status" > "$work/case05-stdin.status"
test "$status" -eq 0 && test ! -s "$work/case05-stdin.stderr"
cmp "$work/case05.expected" "$work/case05-stdin.stdout"
printf 'sipcalc case05 stdin blank/comment/two-address: PASS\n'

printf '%%s\n' '-[ERR : Invalid IPv4 splitmask, unable to split]' '-[ERR : No valid commands recieved]' > "$work/case06-split.expected"
run_case case06-invalid-split 255 -s 33 192.0.2.129/25
cmp "$work/case06-split.expected" "$work/case06-invalid-split.stdout"
printf 'sipcalc case06 pre-resolution invalid splitmask: PASS\n'

sha256sum "$binary" > "$work/binary-after.sha256"
cmp "$work/binary-before.sha256" "$work/binary-after.sha256"
printf 'sipcalc strict CLI: 6 cases PASS\n'
REGRESSION_SCRIPT
cat > expected-version.txt <<'EXPECTED_VERSION'
sipcalc 1.1.6
Written by Simon Ekstrand.

Copyright (C) 2003-2013 Simon Ekstrand.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
EXPECTED_VERSION

%build
%configure
%make_build

%install
%make_install
install -Dpm 0755 run-regressions.sh %{buildroot}%{_libexecdir}/sipcalc/run-regressions.sh
install -Dpm 0644 expected-version.txt %{buildroot}%{_datadir}/sipcalc-tests/expected-version.txt
install -d %{buildroot}%{_licensedir}/%{name}
cp -a source-notices %{buildroot}%{_licensedir}/%{name}/source-notices
install -pm 0644 COPYING GPL-3.0.txt Apache-2.0.txt %{buildroot}%{_licensedir}/%{name}/

%check
set -eu
# Upstream generated check-am only depends on all-am; no TESTS/check_PROGRAMS.
# Preserve its command, while explicitly making no original functional claim.
make check > upstream-check.stdout 2> upstream-check.stderr || { status=$?; cat upstream-check.stdout upstream-check.stderr; exit "$status"; }
cat upstream-check.stdout upstream-check.stderr
bash ./run-regressions.sh "$PWD/src/sipcalc" "$PWD/src/sipcalc" "$PWD/expected-version.txt" > strict-cli.stdout 2> strict-cli.stderr || { status=$?; cat strict-cli.stdout strict-cli.stderr; exit "$status"; }
cat strict-cli.stdout strict-cli.stderr
test ! -s strict-cli.stderr
gawk '/^sipcalc case0[1-6] .*: PASS$/{n++} END{exit(n!=6)}' strict-cli.stdout
test "$(grep -c '^sipcalc strict CLI: 6 cases PASS$' strict-cli.stdout)" -eq 1
# RPM install-post stripping precedes check; bind final installed bytes here.
(cd %{buildroot}; sha256sum ./usr/bin/sipcalc ./usr/libexec/sipcalc/run-regressions.sh ./usr/share/sipcalc-tests/expected-version.txt) > %{buildroot}%{_datadir}/sipcalc-tests/SHA256SUMS

%files
%license %{_licensedir}/%{name}
%doc README NEWS ChangeLog AUTHORS doc/sipcalc.txt
%{_bindir}/sipcalc
%{_mandir}/man1/sipcalc.1*
%{_libexecdir}/sipcalc
%{_datadir}/sipcalc-tests

%changelog
* Tue Oct 27 2026 openEuler RISC-V package contributors - 1.1.6-1
- Preserve upstream defaults and original make check; add six strict CLI cases.
- Correct empty-line indexing, explicit IPv6 argument and bounded stdin storage.
