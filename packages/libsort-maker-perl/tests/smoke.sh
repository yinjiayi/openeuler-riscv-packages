#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libsort-maker-perl
unset PERL5LIB PERLLIB PERL5OPT
/usr/bin/perl - <<'PERL'
use strict;
use warnings;
use Sort::Maker;

my $sorter = make_sorter(qw(plain number descending)) or die $@;
die "incorrect numeric order" unless join(',', $sorter->(2, 10, 3, 2)) eq '10,3,2,2';
print "installed numeric descending sorter passed\n";
PERL
