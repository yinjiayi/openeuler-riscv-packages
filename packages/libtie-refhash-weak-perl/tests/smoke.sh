#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libtie-refhash-weak-perl
unset PERL5LIB PERLLIB PERL5OPT
/usr/bin/perl - <<'PERL'
use strict;
use warnings;
use Tie::RefHash::Weak;

tie my %hash, 'Tie::RefHash::Weak';
{
    my $key = [];
    $hash{$key} = 42;
    die "weak-key entry was not stored" unless keys(%hash) == 1 && $hash{$key} == 42;
}
die "weak-key entry was retained" if keys(%hash);
print "installed weak-key collection passed\n";
PERL
