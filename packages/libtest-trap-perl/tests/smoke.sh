#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-test-trap
perl <<'PERL'
use strict;
use warnings;
use Test::More tests => 3;
use Test::Trap;
trap { print "trapped\n"; exit 7; };
is($trap->stdout, "trapped\n", 'stdout is captured');
is($trap->leaveby, 'exit', 'exit does not terminate the caller');
is($trap->exit, 7, 'the trapped status is preserved');
PERL
