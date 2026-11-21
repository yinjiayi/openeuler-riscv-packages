#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libobject-accessor-perl
unset PERL5LIB PERLLIB PERL5OPT
/usr/bin/perl - <<'PERL'
use strict;
use warnings;
use Object::Accessor;

my $a = Object::Accessor->new('value');
my $b = Object::Accessor->new('value');
$a->value(17);
$b->value(42);
die "objects did not keep separate accessor state" unless $a->value == 17 && $b->value == 42;
print "installed per-object accessors passed\n";
PERL
