#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
perl -MTie::AliasHash -e '
    die "module version" unless $Tie::AliasHash::VERSION eq "1.02";
    tie my %items, "Tie::AliasHash", ["main", "alt"];
    $items{main} = 41;
    die "forward alias" unless $items{alt} == 41;
    $items{alt} = 42;
    die "reverse alias" unless $items{main} == 42;
    (tied %items)->remove_alias("alt");
    die "independent removal" if exists $items{alt};
    die "removed primary" unless $items{main} == 42;
    print "Tie::AliasHash alias mutation and removal passed\n";
'
