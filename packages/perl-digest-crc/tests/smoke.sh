#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-digest-crc
perl -MB -MDigest::CRC=crc32,crc32_hex,crc64 -e '
use strict; use warnings;
die "version" unless $Digest::CRC::VERSION eq "0.24";
die "XS not active" unless B::svref_2object(\&Digest::CRC::_crc)->XSUB;
die "CRC32" unless crc32("123456789") == 3421780262;
die "CRC32 padded hexadecimal" unless crc32_hex("ae") eq "00e7ddce";
die "CRC64" unless crc64("123456789") == 5090661014116757502;
my $ctx = Digest::CRC->new(type => "crc32");
$ctx->add("123"); $ctx->add("456789");
die "incremental checksum" unless $ctx->digest == 3421780262;
print "Digest::CRC installed XS smoke passed\n";
'
