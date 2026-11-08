#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
perl -MHash::SafeKeys -e '
    my %hash = (a => 1, b => 2, c => 3);
    my ($first) = each %hash;
    my @keys = safekeys %hash;
    my ($second) = each %hash;
    my %copy = safecopy %hash;
    my ($third) = each %hash;
    die "hash iterator reset\n" unless @keys == 3
        && defined $second && defined $third
        && $first ne $second && $first ne $third && $second ne $third;
    die "hash copy changed values\n"
        unless join(",", map { $copy{$_} } sort keys %copy) eq "1,2,3";
'
printf '%s\n' 'ok - installed Hash::SafeKeys preserves iterator and copy'
