#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-class-accessor-grouped
perl <<'PERL'
use strict;
use warnings;
use Class::Accessor::Grouped;
die "version" unless $Class::Accessor::Grouped::VERSION eq '0.10014';
{ package SmokeGrouped; our @ISA=('Class::Accessor::Grouped');
  __PACKAGE__->mk_group_accessors(simple => 'value');
  __PACKAGE__->mk_group_ro_accessors(simple => 'fixed');
}
my $object=bless {fixed=>7}, 'SmokeGrouped';
$object->value(0); die "zero value" unless defined($object->value) && $object->value==0;
$object->value('updated'); die "update" unless $object->value eq 'updated';
die "read-only get" unless $object->fixed==7;
my $ok=eval { $object->fixed(9); 1 }; die "read-only setter" if $ok;
print "Grouped accessor smoke passed\n";
PERL
