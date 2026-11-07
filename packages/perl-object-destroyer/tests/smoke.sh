#!/usr/bin/env bash
set -euo pipefail
rpm -q perl-Object-Destroyer
perl <<'PERL'
use strict;
use warnings;
use Object::Destroyer;
die "version mismatch" unless $Object::Destroyer::VERSION eq '2.02';
my $calls = 0;
{ my $guard = Object::Destroyer->new(sub { ++$calls }); }
die "cleanup callback" unless $calls == 1;
{ my $guard = Object::Destroyer->new(sub { ++$calls }); $guard->dismiss; }
die "dismiss callback" unless $calls == 1;
{ package Local::Guarded;
  sub new { bless {released => 0}, shift }
  sub value { 42 }
  sub release { $_[0]{released}++ }
}
my $obj = Local::Guarded->new;
{ my $guard = Object::Destroyer->new($obj, 'release');
  die "wrapper forwarding" unless $guard->value == 42;
}
die "release method" unless $obj->{released} == 1;
my $ok = eval { Object::Destroyer->new(42); 1 };
die "invalid constructor accepted" if $ok;
print "Object::Destroyer installed API smoke passed\n";
PERL
