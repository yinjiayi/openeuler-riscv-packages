#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libtie-shadowhash-perl
unset PERL5LIB PERLLIB PERL5OPT
/usr/bin/perl - <<'PERL'
use strict;
use warnings;
use Tie::ShadowHash;

my $first = {shared => 1};
my $second = {shared => 2, secondary => 3};
tie my %shadow, 'Tie::ShadowHash', $first, $second;
die "unexpected source precedence" unless $shadow{shared} == 1 && $shadow{secondary} == 3;
$shadow{shared} = 9;
delete $shadow{secondary};
die "override or delete leaked" unless $shadow{shared} == 9 && !exists $shadow{secondary}
    && $first->{shared} == 1 && $second->{shared} == 2 && $second->{secondary} == 3;
print "installed shadow precedence and isolated override passed\n";
PERL
