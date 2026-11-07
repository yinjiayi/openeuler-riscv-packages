#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Data-Alias
perl <<'PERL'
use strict;
use warnings;
use Data::Alias qw(alias copy);
die "version" unless $Data::Alias::VERSION eq '1.30';
my $value = 7;
alias my $other = $value;
$other = 11;
die "scalar alias" unless $value == 11;
my @original = (1, 2, 3);
alias my @shared = @original;
$shared[1] = 9;
die "array alias" unless $original[1] == 9;
my @independent = copy @original;
$independent[1] = 4;
die "copy independence" unless $original[1] == 9;
print "Data::Alias installed XS API checks passed\n";
PERL
