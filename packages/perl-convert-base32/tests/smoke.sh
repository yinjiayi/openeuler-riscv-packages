#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Convert-Base32
perl <<'PERL'
use strict;
use warnings;
use Convert::Base32;
die "module version mismatch\n" unless $Convert::Base32::VERSION eq '0.06';
my $bytes = "\x3a\x27\x0f\x93";
die "known encoding mismatch\n" unless encode_base32($bytes) eq 'hitq7ey';
die "case-insensitive decoding mismatch\n" unless decode_base32('HITQ7EY') eq $bytes;
for my $length (1023, 1024, 1025, 1026) {
    my $input = join '', map { chr($_ % 256) } 0 .. $length - 1;
    my $encoded = encode_base32($input);
    die "invalid large-output alphabet\n" unless $encoded =~ /\A[a-z2-7]*\z/;
    die "large round-trip mismatch\n" unless decode_base32($encoded) eq $input;
}
eval { decode_base32('ab') };
die "nonzero padding accepted\n" unless $@ =~ /Padding bits/;
eval { decode_base32('!') };
die "invalid alphabet accepted\n" unless $@ =~ /non-base32/;
print "Convert::Base32 installed API checks passed\n";
PERL
