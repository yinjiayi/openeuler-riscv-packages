#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Algorithm-Annotate
rpm -q --whatprovides 'perl(Algorithm::Annotate)'
perl -MAlgorithm::Annotate -e '
  die "unexpected Algorithm::Annotate version\n"
    unless $Algorithm::Annotate::VERSION eq "0.10";
  my $ann = Algorithm::Annotate->new;
  $ann->init("first", [qw(a b c)]);
  $ann->add("second", [qw(a x c)]);
  my $result = $ann->result;
  die "unexpected annotation result\n"
    unless @$result == 3
      && $result->[0] eq "first"
      && $result->[1] eq "second"
      && $result->[2] eq "first";
'
