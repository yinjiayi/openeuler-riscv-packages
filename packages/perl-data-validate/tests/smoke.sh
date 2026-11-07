#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-data-validate
perl -MData::Validate=is_integer,is_numeric,is_hex,is_between,is_alphanumeric -e '
use strict; use warnings;
die "version" unless $Data::Validate::VERSION eq "0.09";
my $zero = is_integer(0);
die "defined zero" unless defined($zero) && $zero == 0;
die "invalid integer" if defined is_integer("no");
die "numeric" unless is_numeric("1.25") == 1.25;
die "hex normalization" unless is_hex("FF") eq "ff";
die "range" unless is_between(5, 1, 9) == 5;
die "out of range" if defined is_between(10, 1, 9);
die "string" unless is_alphanumeric("abc123") eq "abc123";
die "invalid string" if defined is_alphanumeric("abc-123");
my $v = Data::Validate->new;
die "object" unless $v->is_integer(7) == 7;
print "DataValidate installed API smoke passed\n";
'
