#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-tie-hash-regex
perl -MTie::Hash::Regex -e '
    use strict;
    use warnings;
    die "wrong version" unless $Tie::Hash::Regex::VERSION eq "2.0.0";
    my %hash : Regex;
    $hash{alpha} = "one";
    $hash{beta} = "two";
    die "exact match" unless $hash{alpha} eq "one";
    die "regex match" unless $hash{q(^be)} eq "two";
    die "exists" unless exists $hash{q(^al)};
    die "invalid pattern" if defined $hash{q{(}};
    delete $hash{q(^be)};
    die "delete" if exists $hash{beta};
    die "unrelated key changed" unless $hash{alpha} eq "one";
'
