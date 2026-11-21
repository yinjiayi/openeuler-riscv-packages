#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-object-tiny
perl <<'PERL'
use strict;
use warnings;
use Object::Tiny ();
die "version mismatch\n" unless $Object::Tiny::VERSION eq '1.09';
{ package TinySmoke; use Object::Tiny qw(name count); }
my $object = TinySmoke->new(name => 'rva23', count => 3);
die "constructor/accessor mismatch\n" unless $object->isa('Object::Tiny')
    && $object->name eq 'rva23' && $object->count == 3;
$object->count(9);
die "read-only accessor changed\n" unless $object->count == 3;
eval q{ package InvalidTinySmoke; use Object::Tiny 'bad name'; };
die "invalid accessor accepted\n" unless $@ =~ /Invalid accessor name/;
print "Object::Tiny installed API checks passed\n";
PERL
