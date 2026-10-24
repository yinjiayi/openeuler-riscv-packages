#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
export LC_ALL=C

rpm -q -- csvprintf
rpm -V -- csvprintf
test -x /usr/bin/csvprintf
test -x /usr/bin/xml2csv
test -r /usr/share/csvprintf/csv.xsl
for command in bash diff find grep hexdump mv sed sha256sum sort xsltproc; do
    command -v "$command"
done

qa=/usr/libexec/csvprintf/upstream-tests
test "$(find "$qa/tests" -type f | wc -l)" -eq 85
test "$(wc -l < "$qa/SHA256SUMS")" -eq 86
(cd "$qa" && sha256sum -c SHA256SUMS)

workdir=$(mktemp -d)
trap 'rm -rf -- "$workdir"' EXIT
cp -pr "$qa/tests" "$workdir/tests"
cp "$qa/csv.xsl" "$qa/SHA256SUMS" "$workdir/"
ln -s /usr/bin/csvprintf "$workdir/csvprintf"
(cd "$workdir" && sha256sum -c SHA256SUMS)
# Run both original runners and every original fixture unchanged, using Bash
# transparently for run.sh's pipefail. No eval of csvprintf-generated output.
(cd "$workdir/tests" && bash ./run.sh && bash ./run2.sh)

/usr/bin/csvprintf -v > "$workdir/version.stdout" 2> "$workdir/version.stderr"
test ! -s "$workdir/version.stdout"
grep -Fx 'csvprintf version 1.3.4 (1.3.4)' "$workdir/version.stderr"
/usr/bin/csvprintf -h > "$workdir/help.stdout" 2> "$workdir/help.stderr"
test ! -s "$workdir/help.stdout"
grep -Fx 'Usage:' "$workdir/help.stderr"

printf 'alpha,7\n' > "$workdir/input.csv"
/usr/bin/csvprintf -f "$workdir/input.csv" '%2$02d:%1$s\n' > "$workdir/normal.actual"
printf '07:alpha\n' > "$workdir/normal.expected"
cmp "$workdir/normal.expected" "$workdir/normal.actual"

/usr/bin/csvprintf -x -f "$workdir/input.csv" > "$workdir/input.xml"
/usr/bin/xml2csv "$workdir/input.xml" > "$workdir/roundtrip.actual"
printf '"alpha","7"\n' > "$workdir/roundtrip.expected"
cmp "$workdir/roundtrip.expected" "$workdir/roundtrip.actual"
/usr/bin/xml2csv < "$workdir/input.xml" > "$workdir/roundtrip-stdin.actual"
cmp "$workdir/roundtrip.expected" "$workdir/roundtrip-stdin.actual"

if /usr/bin/csvprintf -x -f "$workdir/missing.csv" > "$workdir/error.stdout" 2> "$workdir/error.stderr"; then
    printf 'missing input unexpectedly succeeded\n' >&2
    exit 1
fi
test -s "$workdir/error.stderr"
