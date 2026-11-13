#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-sort-fields
perl -MSort::Fields -e '
  my @rows = ("first 10", "second 2", "third 2");
  my @sorted = stable_fieldsort(["2n"], @rows);
  die "unexpected stable field order\n"
    unless join("|", @sorted) eq "second 2|third 2|first 10";
  print "installed Sort::Fields stable numeric ordering passed\n";
'
