#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-class-accessor-classy
perl -e '
    package Local::Accessor;
    use Class::Accessor::Classy;
    ro "identity";
    rw "count";
    no Class::Accessor::Classy;
    package main;
    die "unexpected Class::Accessor::Classy version\n"
        unless sprintf("%vd", $Class::Accessor::Classy::VERSION) eq "0.9.1";
    my $obj = bless { identity => "fixed" }, "Local::Accessor";
    $obj->set_count(7);
    die "incorrect accessor behavior\n"
        unless $obj->count == 7 && $obj->identity eq "fixed" && !$obj->can("set_identity");
    print "ok - installed accessors enforce read-only and support read/write\n";
'
