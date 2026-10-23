#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
export LC_ALL=C
unset CHIBI_IGNORE_SYSTEM_PATH TEST_FILTER TEST_REMOVE TEST_GROUP_FILTER TEST_GROUP_REMOVE
export CHIBI_MODULE_PATH=/usr/share/chibi:/usr/lib64/chibi
export LD_LIBRARY_PATH=/usr/lib64
test -x /usr/bin/chibi-scheme
test -s /usr/lib64/libchibi-scheme.so.0.12.0
for tool in chibi-ffi chibi-doc snow-chibi snow-chibi.scm; do
    test -x "/usr/bin/$tool"
done
version=$(/usr/bin/chibi-scheme -V 2>&1)
printf '%s\n' "$version"
printf '%s\n' "$version" | grep -F 'chibi-scheme 0.12.0 '
(
    cd /usr/share/chibi-scheme-tests
    sha256sum -c SHA256SUMS
    test "$(sha256sum r7rs-tests.scm | cut -d ' ' -f 1)" = \
        9b10cac782ef9c52c4cb0a3a489f01415b1262785d7eb14c70fa88ab859cf950
)
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
cd "$work"
# Original upstream suite, now using installed executable and module paths.
/usr/bin/chibi-scheme -mchibi.test \
    -I /usr/share/chibi-scheme-tests -l r7rs-tests.scm -e '(test-exit)'
actual=$(/usr/bin/chibi-scheme -p '(+ (expt 2 64) 1)')
test "$actual" = 18446744073709551617
actual=$(/usr/bin/chibi-scheme -mscheme.char -p '(char=? (char-upcase #\λ) #\Λ)')
test "$actual" = '#t'
printf '%s\n' 'Installed default R7RS suite, bignum and Unicode checks passed.'
