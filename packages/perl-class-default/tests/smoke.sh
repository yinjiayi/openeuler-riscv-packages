#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-class-default
perl <<'PERL'
use strict;
use warnings;
use Class::Default ();
die "version" unless $Class::Default::VERSION eq '1.51';
{ package Smoke::Default; our @ISA=('Class::Default');
  sub new { bless {value=>0}, shift }
  sub value { my $self=shift->_self; $self->{value}=shift if @_; $self->{value} }
}
{ package Smoke::Other; our @ISA=('Smoke::Default'); }
Smoke::Default->value(17);
die "persistent default" unless Smoke::Default->value == 17;
my $object=Smoke::Default->new;
die "instance isolation" unless $object->value == 0;
$object->value(5);
die "default isolation" unless Smoke::Default->value == 17 && $object->value == 5;
die "subclass isolation" unless Smoke::Other->value == 0;
die "class identity" unless $object->_class eq 'Smoke::Default';
print "Class::Default smoke passed\n";
PERL
