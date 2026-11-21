#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
perl -MTie::Hash::ReadonlyStack -e '
    my %source = (shared => "base", kept => "unchanged");
    my $stack = tie my %view, "Tie::Hash::ReadonlyStack", \%source;
    $stack->add_lookup_override_hash("override", {shared => "overlay"});
    $stack->add_lookup_fallback_hash("fallback", {new => "fallback"});
    die "incorrect overlay" unless $view{shared} eq "overlay"
        && $view{kept} eq "unchanged" && $view{new} eq "fallback";
    die "underlying hash was mutated" unless $source{shared} eq "base"
        && $source{kept} eq "unchanged" && !exists $source{new};
    print "ok - installed readonly stack uses override and fallback without mutating source\n";
'
