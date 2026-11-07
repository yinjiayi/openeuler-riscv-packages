#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-accessors
perl -Mstrict -Mwarnings -e '
    { package Smoke::Chained; use accessors qw(value other); }
    { package Smoke::Classic; use accessors::classic qw(value); }
    { package Smoke::ReadOnly; use accessors::ro qw(value); }
    use accessors::chained ();
    use accessors::rw ();
    my $chained = bless {}, "Smoke::Chained";
    die "chaining failed" unless $chained->value("hello")->other(7) == $chained;
    die "getter failed" unless $chained->value eq "hello" && $chained->other == 7;
    my $classic = bless {}, "Smoke::Classic";
    die "classic setter failed" unless $classic->value("world") eq "world";
    my $readonly = bless {value => "fixed"}, "Smoke::ReadOnly";
    die "read-only setter changed value" unless $readonly->value("changed") eq "fixed";
    die "read-only getter failed" unless $readonly->value eq "fixed";
'
