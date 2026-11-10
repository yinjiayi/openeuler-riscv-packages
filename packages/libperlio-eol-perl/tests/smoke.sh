#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libperlio-eol-perl
scratch=$(mktemp -d)
trap 'rm -f -- "$scratch/input"; rmdir -- "$scratch"' EXIT
perl -MPerlIO::eol -e '
    my $path = shift;
    open my $out, ">:raw", $path or die $!;
    print {$out} "A\r\nB\rC\n";
    close $out or die $!;
    open my $in, "<:raw:eol(LF)", $path or die $!;
    local $/;
    die "newline normalization mismatch" unless <$in> eq "A\nB\nC\n";
    print "installed native XS newline normalization passed\n";
' "$scratch/input"
