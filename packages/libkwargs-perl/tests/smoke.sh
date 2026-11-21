#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libkwargs-perl
unset PERL5LIB PERLLIB PERL5OPT
/usr/bin/perl - <<'PERL'
use strict;
use warnings;
use Kwargs qw(kw kwn);

sub mixed { return kwn @_, 1, qw(amount flag) }
sub named { return kw @_, qw(flag amount) }
my @hash = mixed('head', { amount => 23, flag => 0 });
my @flat = mixed('head', flag => 0, amount => 23);
my @named = named(amount => 23, flag => 0);
die "incorrect keyword or positional parsing" unless
    join(':', @hash) eq 'head:23:0' &&
    join(':', @flat) eq 'head:23:0' &&
    join(':', @named) eq '0:23';
print "installed keyword and positional parsing passed\n";
PERL
