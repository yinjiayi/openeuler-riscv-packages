#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-class-exporter
perl <<'PERL'
use strict;
use warnings;
use Class::Exporter;
die "version" unless $Class::Exporter::VERSION eq '0.03';
{ package SmokeObject; our @ISA=('Class::Exporter'); our @EXPORT=qw(value);
  sub new { bless {value=>3}, shift }
  sub value { my $self=shift; $self->{value}=shift if @_; $self->{value} }
}
{ package FirstScope; SmokeObject->import; }
{ package SecondScope; SmokeObject->import; }
die "default" unless FirstScope::value()==3 && SecondScope::value()==3;
FirstScope::value(7); die "state leakage" unless FirstScope::value()==7 && SecondScope::value()==3;
print "Class::Exporter smoke passed\n";
PERL
