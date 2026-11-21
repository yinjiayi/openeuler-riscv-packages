#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
perl -MTest::More=tests,1 -MTest::Carp -e '
    does_croak_that_matches(
        sub { Carp::croak("installed sentinel") }, qr/installed sentinel/
    );
' | awk '
    /^1\.\.1$/ { plan++ }
    /^ok 1 - croak\(\) was called .*installed sentinel/ { pass++ }
    /^not ok/ { fail++ }
    END { exit !(plan == 1 && pass == 1 && !fail) }
'
printf '%s\n' 'ok - installed Test::Carp matches the expected croak'
