#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libdatetime-format-mysql-perl
perl -MDateTime::Format::MySQL -e '
    my $format = "DateTime::Format::MySQL";
    my $sample = "2024-02-29 23:59:57";
    my $parsed = $format->parse_datetime($sample);
    die "unexpected leap-day DateTime" unless $parsed->isa("DateTime")
        && $parsed->year == 2024 && $parsed->month == 2 && $parsed->day == 29;
    die "unexpected date roundtrip" unless $format->format_datetime($parsed) eq $sample;
    print "installed MySQL date roundtrip passed\n";
'
