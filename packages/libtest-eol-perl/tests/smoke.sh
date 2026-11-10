#!/bin/sh
set -eu
tmp=$(mktemp -d)
trap 'rm -f "$tmp/lf.txt"; rmdir "$tmp"' EXIT
printf 'first\nsecond\n' > "$tmp/lf.txt"
perl -MTest::More=tests,1 -MTest::EOL -e 'eol_unix_ok($ARGV[0], "installed EOL checker accepts LF text")' "$tmp/lf.txt"
