#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-class-handle
perl <<'PERL'
use strict;
use warnings;
use Class::Handle ();
die "version" unless $Class::Handle::VERSION eq '1.07';
{ package Smoke::Handle; our $VERSION='2.0'; sub answer {42} }
my $h=Class::Handle->new('Smoke::Handle');
die "name" unless $h->name eq 'Smoke::Handle';
die "class version" unless $h->VERSION eq '2.0';
die "loaded" unless $h->loaded;
die "function" unless $h->can('answer')->()==42;
die "bad name" if Class::Handle->new('9bad');
my $i=Class::Handle->new('Class::Inspector');
die "installed dependency" unless $i->installed && -f $i->loaded_filename;
print "Class::Handle smoke passed\n";
PERL
