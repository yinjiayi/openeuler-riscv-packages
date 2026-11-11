#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-convert-nls-date-format
perl -MConvert::NLS_DATE_FORMAT -e '
    my $oracle = "YYYY-MM-DD HH24:MI:SS";
    my $posix = "%Y-%m-%d %H:%M:%S";
    die "Oracle to POSIX conversion failed\n"
        unless Convert::NLS_DATE_FORMAT::oracle2posix($oracle) eq $posix;
    die "POSIX to Oracle conversion failed\n"
        unless Convert::NLS_DATE_FORMAT::posix2oracle($posix) eq $oracle;
    print "Convert::NLS_DATE_FORMAT smoke passed\n";
'
