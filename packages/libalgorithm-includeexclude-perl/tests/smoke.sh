#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Algorithm-IncludeExclude
rpm -q --whatprovides 'perl(Algorithm::IncludeExclude)'
perl -MAlgorithm::IncludeExclude -e '
  die "unexpected Algorithm::IncludeExclude version\n"
    unless $Algorithm::IncludeExclude::VERSION eq "0.01";
  my $rules = Algorithm::IncludeExclude->new;
  $rules->include();
  $rules->exclude("private");
  $rules->include(qw(private public));
  die "exclude rule failed\n" if $rules->evaluate(qw(private hidden));
  die "nested include rule failed\n"
    unless $rules->evaluate(qw(private public file));
  die "default include rule failed\n"
    unless $rules->evaluate(qw(other file));
'
