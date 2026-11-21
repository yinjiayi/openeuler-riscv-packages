#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-test-nobreakpoints
fixture_dir=$(mktemp -d)
trap 'rm -f -- "$fixture_dir/clean.pl"; rmdir -- "$fixture_dir"' EXIT
printf '%s\n' '#!/usr/bin/env perl' 'print "clean source\\n";' > "$fixture_dir/clean.pl"
perl -MTest::Builder -MTest::NoBreakpoints -e '
    Test::Builder->new->plan(tests => 1);
    exit(no_breakpoints_ok($ARGV[0], "installed module accepts clean Perl source") ? 0 : 1);
' "$fixture_dir/clean.pl"
