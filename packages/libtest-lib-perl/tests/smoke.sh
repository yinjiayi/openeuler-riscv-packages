#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
fixture=$(mktemp -d "${TMPDIR:-/tmp}/test-lib-smoke.XXXXXXXX")
trap 'rm -f -- "$fixture/t/lib/LocalWitness.pm" "$fixture/t/deep/smoke.pl"; rmdir -- "$fixture/t/lib" "$fixture/t/deep" "$fixture/t" "$fixture"' EXIT
mkdir -p "$fixture/t/lib" "$fixture/t/deep"
printf '%s\n' 'package LocalWitness;' 'sub answer { 42 }' '1;' > "$fixture/t/lib/LocalWitness.pm"
printf '%s\n' 'use strict;' 'use warnings;' 'use Test::Lib;' 'require LocalWitness;' \
    'die "private fixture path was not found" unless LocalWitness::answer() == 42;' \
    'print "ok - installed Test::Lib finds its private fixture\n";' > "$fixture/t/deep/smoke.pl"
perl "$fixture/t/deep/smoke.pl"
