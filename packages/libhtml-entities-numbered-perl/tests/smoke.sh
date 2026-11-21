#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libhtml-entities-numbered-perl
/usr/bin/perl - <<'PERL'
use strict;
use warnings;
use HTML::Entities::Numbered;

die "unexpected HTML reference conversion\n"
    unless name2hex('&hearts;') eq '&#x2665;' && hex2name('&#x2665;') eq '&hearts;';
die "unexpected XML reference conversion\n"
    unless name2decimal_xml('&apos; &hearts; &unknown;') eq '&apos; &#9829; &unknown;';
print "installed HTML roundtrip and XML preservation passed\n";
PERL
