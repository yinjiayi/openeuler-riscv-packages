#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Number-Bytes-Human
perl <<'PERL'
use strict;
use warnings;
use Number::Bytes::Human qw(format_bytes parse_bytes);
die "module version mismatch\n" unless $Number::Bytes::Human::VERSION eq '0.11';
die "zero format mismatch\n" unless format_bytes(0) eq '0';
die "binary unit mismatch\n" unless format_bytes(1024) eq '1.0K';
die "fraction format mismatch\n" unless format_bytes(1536) eq '1.5K';
die "binary parse mismatch\n" unless parse_bytes('1.5G') == 1610612736;
my $human = Number::Bytes::Human->new(bs => 1000, si => 1);
die "decimal format mismatch\n" unless $human->format(1E7) eq '10MB';
die "decimal parse mismatch\n" unless $human->parse('10MB') == 1E7;
$human->set_options(zero => '-');
die "custom zero format mismatch\n" unless $human->format(0) eq '-';
die "custom zero parse mismatch\n" unless $human->parse('-') == 0;
print "Number::Bytes::Human installed API checks passed\n";
PERL
