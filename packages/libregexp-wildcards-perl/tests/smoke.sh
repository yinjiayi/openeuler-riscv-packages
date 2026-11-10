#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libregexp-wildcards-perl
perl -MRegexp::Wildcards -e '
    die "unexpected installed version" unless Regexp::Wildcards->VERSION eq "1.05";
    my $wildcards = Regexp::Wildcards->new;
    $wildcards->do(set => ["jokers"]);
    my $rx = $wildcards->convert(q{foo*.txt});
    die "wildcard did not match the text filename" unless "foobar.txt" =~ /\A$rx\z/;
    die "wildcard matched the wrong extension" if "foobar.html" =~ /\A$rx\z/;
'
