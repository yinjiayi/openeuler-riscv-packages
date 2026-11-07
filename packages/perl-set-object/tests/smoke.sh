#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-set-object
perl -MSet::Object=set,weak_set -e '
use strict; use warnings;
die "version" unless $Set::Object::VERSION == 1.43;
my $a=set(1,2,2,3); my $b=set(3,4);
die "unique" unless $a->size == 3;
die "union" unless ($a+$b)->size == 4;
die "intersection" unless ($a*$b)->size == 1 && ($a*$b)->includes(3);
die "difference" unless ($a-$b)->size == 2;
my $obj={a=>1}; my $weak=weak_set($obj);
die "weak start" unless $weak->size == 1;
undef $obj; die "weak release" unless $weak->size == 0;
print "SetObject installed API smoke passed\n";
'
