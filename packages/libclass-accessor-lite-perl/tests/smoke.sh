#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-class-accessor-lite
perl <<'PERL'
use strict;
use warnings;
{
    package Smoke;
    use Class::Accessor::Lite (new => 1, rw => ['value'], ro => ['fixed'], wo => ['sink']);
}
die "version mismatch" unless $Class::Accessor::Lite::VERSION eq '0.08';
my $object = Smoke->new(value => 3, fixed => 7);
die "getter" unless $object->value == 3;
die "setter" unless $object->value(9) == 9 && $object->value == 9;
die "read-only getter" unless $object->fixed == 7;
eval { $object->fixed(1) };
die "read-only setter accepted" unless $@;
$object->sink(11);
die "write-only setter" unless $object->{sink} == 11;
eval { $object->sink };
die "write-only getter accepted" unless $@;
$object->value(4, 5);
die "multi-value accessor" unless ref($object->value) eq 'ARRAY' && $object->value->[1] == 5;
print "Class::Accessor::Lite installed smoke passed\n";
PERL
