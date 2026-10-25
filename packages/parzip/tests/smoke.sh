#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- parzip
test -x /usr/bin/parzip
test -x /usr/bin/parunzip
test -x /usr/libexec/parzip-tests/bytequeue_test
test -s /usr/share/man/man1/parzip.1.gz
test -s /usr/share/man/man1/parunzip.1.gz
suite=/usr/share/parzip-tests
notices=/usr/share/licenses/parzip
test -s "$notices/COPYING"
test -s "$notices/original-notices.sha256"
(cd "$notices/original-notices" && sha256sum -c ../original-notices.sha256)
(cd "$suite" && sha256sum -c original-tests.sha256)
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
cd "$work"
# Original strict ST_ASSERT exits nonzero on failure; Python uses unittest.
/usr/libexec/parzip-tests/bytequeue_test > bytequeue.log 2>&1
cat bytequeue.log
python3 -B "$suite/test/unziptest.py" "$suite" /usr/bin
python3 -B "$suite/test/ziptest.py" "$suite" /usr/bin
