#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
perl <<'PERL'
use strict;
use warnings;
use Class::WhiteHole;
{
    package SmokeAutoload;
    our $calls = 0;
    sub AUTOLOAD { ++$calls; return 'unwanted fallback'; }
}
{
    package SmokeChild;
    our @ISA = ('Class::WhiteHole', 'SmokeAutoload');
    sub static_method { return 'preserved'; }
}
die "version mismatch\n" unless $Class::WhiteHole::VERSION eq '0.04';
die "static method changed\n" unless SmokeChild->static_method eq 'preserved';
die "can changed\n" unless ref(SmokeChild->can('static_method')) eq 'CODE';
eval { SmokeChild->absent_method(); };
die "missing method not rejected\n"
    unless $@ =~ /Can't locate object method "absent_method" via package "SmokeChild"/;
eval { my $object = bless {}, 'SmokeChild'; };
die "DESTROY failed\n" if $@;
die "inherited AUTOLOAD invoked\n" if $SmokeAutoload::calls;
print "Class::WhiteHole static/can/AUTOLOAD rejection/DESTROY smoke passed\n";
PERL
