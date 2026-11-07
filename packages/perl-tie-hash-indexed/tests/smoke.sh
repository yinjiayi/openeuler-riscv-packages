#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-tie-hash-indexed
perl -MTie::Hash::Indexed -e '
    die "version" unless $Tie::Hash::Indexed::VERSION eq "0.08";
    tie my %h, "Tie::Hash::Indexed";
    $h{second}=2; $h{first}=1; $h{third}=3;
    die "order" unless join(",",keys %h) eq "second,first,third";
    $h{first}=10;
    die "update" unless $h{first} == 10 && join(",",keys %h) eq "second,first,third";
    delete $h{second};
    die "delete" unless join(",",keys %h) eq "first,third";
'
