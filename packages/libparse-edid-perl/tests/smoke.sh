#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-parse-edid

perl -MParse::EDID -e '
    my @edid = (0, (255) x 6, 0, 6, 175, 20, 161, (0) x 116);
    @edid[18,19] = (1,3);
    my $sum = 0;
    $sum += $_ for @edid;
    $edid[127] = (-$sum) & 255;
    my $display = parse_edid(pack("C*", @edid));
    die "synthetic EDID manufacturer or identifier was incorrect\n"
        unless $display->{manufacturer_name} eq "AUO"
            && $display->{EISA_ID} eq "AUOa114"
            && $display->{product_code} == 41236;
    print "ok 1 - installed EDID parser identifies the synthetic AUO display\n";
'
