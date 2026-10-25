#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-List-Gen
rpm -q --whatprovides 'perl(List::Gen)'
rpm -q --whatprovides 'perl(List::Generator)'
perl -MList::Gen=range -e '
  die "unexpected List::Gen version\n"
    unless $List::Gen::VERSION eq "0.979";
  my $numbers = range(1, 3);
  die "generator result mismatch\n"
    unless join(",", $numbers->all) eq "1,2,3";
'
