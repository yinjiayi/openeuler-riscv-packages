#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libregexp-optimizer-perl
unset PERL5LIB PERLLIB PERL5OPT
/usr/bin/perl -MRegexp::Optimizer -MRegexp::List - <<'PERL'
use strict;
use warnings;

my $opt = Regexp::Optimizer->new->optimize(qr/\A(?:foobar|fooxar|foozap)\z/);
my $list = Regexp::List->new->list2re(qw(\Acat\z \Acar\z));
die "optimized alternatives failed" unless 'fooxar' =~ $opt && 'foobaz' !~ $opt;
die "legacy list alternatives failed" unless 'car' =~ $list && 'can' !~ $list;
print "installed regex optimization and legacy list passed\n";
PERL
