#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- spiped
export LC_ALL=C.UTF-8
export PATH=/usr/bin:/bin
unset N USE_VALGRIND USE_VALGRIND_NO_REGEN TEST_DNSTHREAD_ENABLE_REMOTE

qa=/usr/libexec/spiped-qa
test -x /usr/bin/spiped
test -x /usr/bin/spipe
test -r /dev/urandom
test "$(readlink "$qa/spiped/spiped")" = /usr/bin/spiped
test "$(readlink "$qa/spipe/spipe")" = /usr/bin/spipe
(cd "$qa" && sha256sum -c tests.sha256)
for helper in \
    tests/dnsthread-resolve/dnsthread-resolve \
    tests/msleep/msleep \
    tests/nc-client/nc-client \
    tests/nc-server/nc-server \
    tests/pthread_create_blocking_np/test_pthread_create_blocking_np \
    tests/pushbits/test_pushbits \
    tests/valgrind/potential-memleaks; do
    test -x "$qa/$helper"
done

# The upstream driver finds its binaries relative to itself; the packaged
# symlinks above bind both endpoints to installed binaries, not build outputs.
# Run from a fresh short path to keep UNIX socket names within platform limits.
spiped_qa_work=$(mktemp -d /tmp/spiped-qa.XXXXXXXX)
trap 'rm -rf -- "$spiped_qa_work"' EXIT
cd "$spiped_qa_work"
if timeout --kill-after=30 1800 "$qa/tests/test_spiped.sh" >qa.stdout 2>qa.stderr; then
    cat qa.stdout qa.stderr
else
    spiped_qa_exit=$?
    cat qa.stdout qa.stderr
    exit "$spiped_qa_exit"
fi

# Unlike an uninstalled source build, a packaged smoke run has system spiped.
# Retain the upstream conditional unchanged, but require all ten scenarios here.
test "$(grep -cE '^  [0-9][0-9]-.*SUCCESS!$' qa.stderr)" -eq 10
if grep -E 'SKIP!|FAILED!|PARTIAL SUCCESS' qa.stderr; then
    exit 1
fi
