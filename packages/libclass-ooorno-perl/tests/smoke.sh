#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-class-ooorno
perl -MClass::OOorNO=shave_opts -e '
    die "unexpected Class::OOorNO version\n"
        unless $Class::OOorNO::VERSION eq "0.011";
    my @args = ("--name=test", "plain");
    my $opts = shave_opts(\@args);
    die "argument classification failed\n"
        unless $opts->{"--name"} eq "test" && @args == 1 && $args[0] eq "plain";
    print "ok - installed OOorNO separates options and positional arguments\n";
'
