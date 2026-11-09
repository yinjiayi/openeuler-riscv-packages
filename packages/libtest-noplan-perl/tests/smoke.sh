#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
scratch="$(mktemp -d -- "${TMPDIR:-/tmp}/test-noplan.XXXXXX")"
trap 'rm -f -- "$scratch/planned.t" "$scratch/unplanned.t"; rmdir -- "$scratch"' EXIT
printf '%s\n' 'use Test::More tests => 1;' > "$scratch/planned.t"
printf '%s\n' "use Test::More 'no_plan';" > "$scratch/unplanned.t"
perl -MTest::NoPlan=check_file_for_no_plan -e '
    die "fixed plan was rejected" unless check_file_for_no_plan($ARGV[0]);
    die "explicit no_plan was accepted" if check_file_for_no_plan($ARGV[1]);
    print "ok 1 - installed checker accepts a fixed test plan\nok 2 - installed checker detects an explicit no_plan\n";
' "$scratch/planned.t" "$scratch/unplanned.t"
