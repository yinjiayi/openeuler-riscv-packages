#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-sub-override
perl -MSub::Override -e '
    die "unexpected Sub::Override version\n" unless $Sub::Override::VERSION eq "0.12";
    sub Local::Example::value { 23 }
    my $guard = Sub::Override->new("Local::Example::value", sub { 42 });
    die "override failed\n" unless Local::Example::value() == 42;
    $guard->restore;
    die "restore failed\n" unless Local::Example::value() == 23;
    print "ok - installed subroutine override and restore\n";
'
