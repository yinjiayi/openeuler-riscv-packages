#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
perl <<'PERL'
use strict;
use warnings;
{
    package SmokeParent;
    use Class::AutoloadCAN;
    sub CAN {
        my ($class, $method) = @_;
        return sub { shift; return join(':', 'inherited', @_); }
            if $method eq 'dynamic_method';
        return;
    }
}
{
    package SmokeChild;
    our @ISA = ('SmokeParent');
}
die "version mismatch\n" unless $Class::AutoloadCAN::VERSION == 0.03;
my $code = SmokeChild->can('dynamic_method');
die "inherited can failed\n" unless ref($code) eq 'CODE';
die "inherited dispatch failed\n"
    unless SmokeChild->dynamic_method('RVA23') eq 'inherited:RVA23';
die "can callback failed\n"
    unless $code->('SmokeChild', 'SP3') eq 'inherited:SP3';
die "missing method advertised\n" if SmokeChild->can('absent_method');
eval { SmokeChild->absent_method(); };
die "missing method did not fail\n" unless $@ =~ /Can't locate object method/;
print "Class::AutoloadCAN inherited dispatch, can and negative-call smoke passed\n";
PERL
