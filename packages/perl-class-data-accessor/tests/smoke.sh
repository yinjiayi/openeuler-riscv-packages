#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-class-data-accessor
perl <<'PERL'
use strict;
use warnings;
use Class::Data::Accessor ();
die "version" unless $Class::Data::Accessor::VERSION eq '0.04004';
{ package Smoke::Parent; our @ISA=('Class::Data::Accessor'); __PACKAGE__->mk_classaccessor(value=>11); }
{ package Smoke::Child; our @ISA=('Smoke::Parent'); }
die "inheritance" unless Smoke::Child->value == 11;
Smoke::Child->value(22);
die "class override" unless Smoke::Child->value == 22 && Smoke::Parent->value == 11;
my $object=bless {},'Smoke::Child';
die "instance fallback" unless $object->value == 22;
$object->value(33);
die "instance isolation" unless $object->value == 33 && Smoke::Child->value == 22;
eval { $object->mk_classaccessor('bad') }; die "invalid instance constructor" unless $@;
print "Class::Data::Accessor smoke passed\n";
PERL
