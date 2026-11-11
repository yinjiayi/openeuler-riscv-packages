#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-test-is
perl -MTest::Is -e 'exit 0' >/dev/null 2>&1 && exit 1
plain=$(NONINTERACTIVE_TESTING=0 perl -e 'use Test::Is "interactive"; print "run"')
skipped=$(NONINTERACTIVE_TESTING=1 perl -e 'use Test::Is "interactive"; print "not reached"')
test "$plain" = run
test "$skipped" = '1..0 # SKIP interactive test'
printf '%s\n' 'installed Test::Is interactive context and TAP skip protocol passed'
