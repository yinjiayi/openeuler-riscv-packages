#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-sort-versions
perl -MSort::Versions -e '
    die "unexpected module version\n" unless $Sort::Versions::VERSION eq "1.62";
    die "incorrect pairwise comparison\n" unless versioncmp("1.9", "1.10") < 0;
    my @ordered = sort versions qw(2.10 1.9 1.10);
    die "incorrect ordering\n" unless join(",", @ordered) eq "1.9,1.10,2.10";
    print "ok - installed numeric version ordering\n";
'
