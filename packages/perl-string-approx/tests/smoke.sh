#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-string-approx
perl <<'PERL'
use strict;
use warnings;
use String::Approx qw(aindex arindex adist);
die "version mismatch\n" unless $String::Approx::VERSION eq '3.28';
die "exact index mismatch\n" unless aindex('xyz', 'abcdefxyz') == 6;
die "approximate index mismatch\n" unless aindex('xyz', 'abcdefxgz') == 6;
die "reverse index mismatch\n" unless arindex('xyz', 'abcxyzdefxyz') == 9;
die "edit distance mismatch\n" unless adist('abc', 'abd') == 1;
die "empty input mismatch\n" unless adist('', 'abc') == 3;
print "String::Approx installed XS API checks passed\n";
PERL
