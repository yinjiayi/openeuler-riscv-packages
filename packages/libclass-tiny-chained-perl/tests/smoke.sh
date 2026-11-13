#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-class-tiny-chained
perl -e '
    package SmokeChain;
    use Class::Tiny::Chained q(value);
    package main;
    die "unexpected module version" unless $Class::Tiny::Chained::VERSION eq "0.004";
    my $o = SmokeChain->new;
    die "bad chain" unless $o->value("alpha") == $o && $o->value eq "alpha";
    print "installed chained setter and getter work\n";
'
