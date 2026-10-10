#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Set-IntSpan
rpm -q --whatprovides 'perl(Set::IntSpan)'
module_file="$(perl -MSet::IntSpan -e 'print $INC{"Set/IntSpan.pm"}')"
test -n "$module_file"
rpm -qf -- "$module_file"

perl -MSet::IntSpan -e '
  die "unexpected version\n" unless $Set::IntSpan::VERSION eq "1.19";
  my $left = Set::IntSpan->new("1-3,7");
  my $right = Set::IntSpan->new("3-5");
  die "membership failed\n" unless $left->member(3) && !$left->member(4);
  die "union failed\n" unless $left->union($right)->run_list eq "1-5,7";
  die "intersection failed\n" unless $left->intersect($right)->run_list eq "3";
  die "difference failed\n" unless $left->diff($right)->run_list eq "1-2,7";
  die "source set mutated\n"
    unless $left->run_list eq "1-3,7" && $right->run_list eq "3-5";
'
