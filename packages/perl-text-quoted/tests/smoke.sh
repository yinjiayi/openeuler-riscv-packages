#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-text-quoted
/usr/bin/perl -MText::Quoted=extract -e '
    die "version" unless $Text::Quoted::VERSION eq "2.10";
    my $parsed = extract("> packaged quote\n");
    die "quoted text" unless ref($parsed) eq "ARRAY" && @$parsed == 1
        && ref($parsed->[0]) eq "ARRAY" && @{$parsed->[0]} == 1
        && ref($parsed->[0][0]) eq "HASH"
        && $parsed->[0][0]{text} eq "packaged quote"
        && $parsed->[0][0]{quoter} eq ">";
'
