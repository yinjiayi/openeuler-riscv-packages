#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-class-accessor-class
perl <<'PERL'
use strict;
use warnings;
use Class::Accessor::Class;
die "version" unless $Class::Accessor::Class::VERSION eq '0.504';
{ package Probe; use parent 'Class::Accessor::Class'; __PACKAGE__->mk_class_accessors('shared'); }
my $a=Probe->new; my $b=Probe->new;
Probe->shared(12);
die "shared initial" unless $a->shared==12 && $b->shared==12;
$a->shared(0);
die "shared false value" unless defined(Probe->shared) && Probe->shared==0 && $b->shared==0;
print "Class::Accessor::Class smoke passed\n";
PERL
