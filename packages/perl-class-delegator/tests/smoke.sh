#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-class-delegator
perl <<'PERL'
use strict;
use warnings;
use Class::Delegator ();
die "version" unless $Class::Delegator::VERSION eq '0.09';
{ package Smoke::Leaf;
  sub new { bless { value => $_[1] }, $_[0] }
  sub value { my $s=shift; $s->{value}=shift if @_; return $s->{value}; }
}
{ package Smoke::Single;
  use Class::Delegator send => 'read', to => '{leaf}', as => 'value';
  sub new { bless { leaf => Smoke::Leaf->new(7) }, $_[0] }
}
{ package Smoke::Many;
  use Class::Delegator send => 'value', to => ['{left}', '{right}'];
  sub new { bless { left=>Smoke::Leaf->new(3), right=>Smoke::Leaf->new(5) }, $_[0] }
}
my $s=Smoke::Single->new;
die "single delegation" unless $s->read==7 && $s->read(9)==9;
my $m=Smoke::Many->new;
my $scalar=$m->value;
die "scalar multi" unless ref($scalar) eq 'ARRAY' && join(',',@$scalar) eq '3,5';
my @list=$m->value;
die "list multi" unless @list==2 && $list[0][0]==3 && $list[1][0]==5;
die "mutating multi" unless join(',',@{$m->value(11)}) eq '11,11';
PERL
