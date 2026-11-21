#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
fixture=$(mktemp)
trap 'rm -f -- "$fixture"' EXIT
printf '%s\n' 'use strict;' 'use warnings;' 'my $value = 42;' > "$fixture"
perl -MTest::More=tests,3 -MTest::Strict -e '
    Test::Strict::syntax_ok($ARGV[0]) or exit 1;
    Test::Strict::strict_ok($ARGV[0]) or exit 1;
    Test::Strict::warnings_ok($ARGV[0]) or exit 1;
' "$fixture"
