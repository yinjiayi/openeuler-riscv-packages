#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libencode-zapcp1252-perl
unset PERL5LIB PERLLIB PERL5OPT
/usr/bin/perl - <<'PERL'
use strict;
use warnings;
use Encode qw(decode FB_CROAK);
use Encode::ZapCP1252 qw(fix_cp1252 zap_cp1252);

my $input = chr(0x80);
my $utf8_bytes = fix_cp1252($input);
my $ascii = zap_cp1252($input);
die "wrong conversion" unless
    decode('UTF-8', $utf8_bytes, FB_CROAK) eq chr(0x20AC) &&
    $ascii eq 'e' && $input eq chr(0x80);
print "installed CP1252 Unicode and ASCII conversion passed\n";
PERL
