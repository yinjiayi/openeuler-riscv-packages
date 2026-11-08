#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libxml-dumper-perl
scratch=$(mktemp -d)
trap 'rm -f -- "$scratch/roundtrip.xml.gz"; rmdir -- "$scratch"' EXIT
perl -MXML::Dumper -e '
    die "unexpected installed version" unless XML::Dumper->VERSION eq "0.81";
    my $xml = XML::Dumper->new();
    my $input = {key => "riscv"};
    my $plain = $xml->xml2pl($xml->pl2xml($input));
    die "plain roundtrip failed" unless $plain->{key} eq "riscv";
    $xml->pl2xml($input, $ARGV[0]);
    open my $fh, "<:raw", $ARGV[0] or die $!;
    my $header;
    die "not a gzip file" unless read($fh, $header, 2) == 2 && $header eq "\x1f\x8b";
    close $fh or die $!;
    my $compressed = $xml->xml2pl($ARGV[0]);
    die "gzip roundtrip failed" unless $compressed->{key} eq "riscv";
' "$scratch/roundtrip.xml.gz"
