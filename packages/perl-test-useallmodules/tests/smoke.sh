#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-test-useallmodules
testdir=$(mktemp -d)
trap 'rm -f -- "$testdir/MANIFEST"; rmdir -- "$testdir"' EXIT
printf '%s\n' 'lib/Test/UseAllModules.pm' > "$testdir/MANIFEST"
(
  cd "$testdir"
  perl -MTest::UseAllModules -e '
    die "unexpected version" unless $Test::UseAllModules::VERSION eq "0.17";
    all_uses_ok();
  '
)
