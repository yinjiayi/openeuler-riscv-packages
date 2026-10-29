#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-List-Maker
rpm -q --whatprovides 'perl(List::Maker)'
perl -MList::Maker -e '
  die "unexpected List::Maker version\n"
    unless $List::Maker::VERSION eq "0.005";
  my @values = <1..3>;
  die "list construction mismatch\n"
    unless join(",", @values) eq "1,2,3";
'
