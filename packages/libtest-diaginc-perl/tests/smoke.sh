#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-test-diaginc

smoke_tmp="$(mktemp -d)"
trap 'rm -f -- "$smoke_tmp/stdout" "$smoke_tmp/stderr"; rmdir -- "$smoke_tmp"' EXIT
rc=0
perl -MTest::DiagINC -MFile::Spec -e 'exit 7' >"$smoke_tmp/stdout" 2>"$smoke_tmp/stderr" || rc=$?
test "$rc" -eq 7
test ! -s "$smoke_tmp/stdout"
grep -Fq 'Listing modules from %INC' "$smoke_tmp/stderr"
grep -Eq '[0-9.]+ +File::Spec([[:space:]]|$)' "$smoke_tmp/stderr"
printf '%s\n' 'ok 1 - installed DiagINC reports loaded module and preserves exit 7'
