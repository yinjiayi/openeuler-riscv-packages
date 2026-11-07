#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-class-observable
perl <<'PERL'
use strict;
use warnings;
use Class::Observable ();
die "version" unless $Class::Observable::VERSION eq '2.004';
{ package Smoke::Observable; our @ISA=('Class::Observable'); }
my $object=bless {}, 'Smoke::Observable';
my @events;
my $observer=sub { my($observed,$event)=@_; push @events,$event; };
$object->add_observer($observer);
die "registration" unless $object->count_observers==1;
$object->notify_observers('first');
die "notification" unless @events==1 && $events[0] eq 'first';
my $copy=bless {}, 'Smoke::Observable';
die "copy" unless $object->copy_observers($copy)==1;
$copy->notify_observers('copied');
die "copy notification" unless @events==2 && $events[1] eq 'copied';
$object->delete_observer($observer);
die "deletion" unless $object->count_observers==0;
die "remove all" unless $copy->delete_all_observers==1;
print "Class::Observable smoke passed\n";
PERL
