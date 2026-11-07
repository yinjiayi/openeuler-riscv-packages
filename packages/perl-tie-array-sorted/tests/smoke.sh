#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Tie-Array-Sorted
perl -MTie::Array::Sorted -MTie::Array::Sorted::Lazy -e '
    die "version" unless $Tie::Array::Sorted::VERSION eq "1.41";
    for my $class (qw(Tie::Array::Sorted Tie::Array::Sorted::Lazy)) {
        tie my @values, $class, sub { $_[0] <=> $_[1] };
        push @values, 10, 4, 7, 3, 4;
        die "$class ordering" unless "@values" eq "3 4 4 7 10";
        die "$class pop" unless pop(@values) == 10;
        unshift @values, 1;
        die "$class mutation" unless "@values" eq "1 3 4 4 7";
    }
'
