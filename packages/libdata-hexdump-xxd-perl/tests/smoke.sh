#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
perl -MData::HexDump::XXD=xxd,xxd_r -e '
    my $bytes = "A\0\xFF\n";
    my $dump = xxd($bytes);
    die "unexpected xxd grouping\n" unless $dump =~ /^0000000: 4100 ff0a/m;
    die "binary round trip changed bytes\n" unless xxd_r($dump) eq $bytes;
'
printf '%s\n' 'ok - installed Data::HexDump::XXD preserves byte grouping and roundtrip'
