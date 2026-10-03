#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Clone-PP
rpm -q --whatprovides 'perl(Clone::PP)'
perl -MClone::PP=clone -e '
  die "unexpected Clone::PP version\n" unless $Clone::PP::VERSION eq "1.09";
  my $source = { items => [1, { label => "original" }] };
  my $copy = clone($source);
  die "copy has wrong structure\n"
    unless $copy->{items}[0] == 1 && $copy->{items}[1]{label} eq "original";
  $copy->{items}[1]{label} = "changed";
  die "clone shares nested hash\n"
    unless $source->{items}[1]{label} eq "original";
'
