#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-class-can
perl <<'PERL'
use strict;
use warnings;
use Class::Can;
die "version" unless $Class::Can::VERSION eq '0.01';
{ package SmokeBase; sub base_method {} sub shared_method {} }
{ package SmokeChild; our @ISA=('SmokeBase'); sub shared_method {} sub child_method {} }
my %methods=Class::Can->interrogate('SmokeChild');
die "inheritance" unless $methods{base_method} eq 'SmokeBase';
die "override" unless $methods{shared_method} eq 'SmokeChild';
die "child" unless $methods{child_method} eq 'SmokeChild';
die "method count" unless keys(%methods)==3;
print "Class::Can smoke passed\n";
PERL
