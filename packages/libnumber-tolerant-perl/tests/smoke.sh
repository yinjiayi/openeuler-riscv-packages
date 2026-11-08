#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
perl -MNumber::Tolerant=tolerance -MTest::More=tests,2 -MTest::Tolerant -e '
    my $range = tolerance(10, "plus_or_minus", 1);
    ok(10 == $range && !(12 == $range), "numeric tolerance excludes outside");
    is_tol(10, $range, "installed Test::Tolerant agrees");
' | awk '
    /^1\.\.2$/ { plan++ }
    /^ok 1 - numeric tolerance excludes outside$/ { outside++ }
    /^ok 2 - installed Test::Tolerant agrees$/ { inside++ }
    /^not ok/ { fail++ }
    END { exit !(plan == 1 && outside == 1 && inside == 1 && !fail) }
'
printf '%s\n' 'ok - installed Number::Tolerant and Test::Tolerant agree'
