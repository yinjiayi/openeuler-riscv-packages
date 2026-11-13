#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-sort-naturally
perl -MSort::Naturally -e '
    die "unexpected module version" unless $Sort::Naturally::VERSION eq "1.03";
    die "natural order failed" unless join(",", nsort(qw(file10 file2 file1))) eq "file1,file2,file10";
    die "numeric comparison failed" unless ncmp("item9", "item11") < 0;
    print "installed Sort::Naturally order and comparison passed\n";
'
