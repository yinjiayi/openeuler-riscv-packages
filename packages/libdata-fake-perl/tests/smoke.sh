#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
perl -MData::Fake::Core -e '
    my $int = fake_int(4,8);
    for (1..25) {
        my $v = $int->();
        die "outside inclusive bounds" if $v < 4 || $v > 8 || int($v) != $v;
    }
    die "singleton choice changed" if fake_pick("sentinel")->() ne "sentinel";
    die "unexpected identifier pattern" unless fake_digits("ID-###")->() =~ /\AID-[0-9]{3}\z/;
    print "ok 1 - installed fake integers respect inclusive bounds\nok 2 - installed pick preserves singleton and digit pattern\n";
'
