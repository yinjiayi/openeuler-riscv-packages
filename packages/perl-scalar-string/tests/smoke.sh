#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-scalar-string
perl <<'PERL'
use strict;
use warnings;
use Scalar::String qw(sclstr_is_upgraded sclstr_is_downgraded sclstr_upgraded sclstr_downgraded);
die "version mismatch\n" unless $Scalar::String::VERSION eq '0.003';
my $plain = "a\x00b\xff";
my $up = sclstr_upgraded($plain);
die "upgrade mismatch\n" unless sclstr_is_upgraded($up) && $up eq $plain;
my $down = sclstr_downgraded($up);
die "downgrade mismatch\n" unless sclstr_is_downgraded($down) && $down eq $plain;
my $wide = "a\x{100}b";
eval { sclstr_downgraded($wide) };
die "wide character unexpectedly downgraded\n" unless $@;
die "fail_ok changed wide characters\n" unless sclstr_downgraded($wide, 1) eq $wide;
print "Scalar::String encoding smoke passed\n";
PERL
