#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-Sah-Normalize
rpm -q --whatprovides 'perl(Data::Sah::Normalize)'
perl -MData::Sah::Normalize=normalize_clset,normalize_schema -e '
  die "wrong installed version\n"
    unless $Data::Sah::Normalize::VERSION eq "0.051";
  my $clset = normalize_clset({"!ready" => 1, "choice|" => [2, 3]});
  die "clause normalization failed\n"
    unless $clset->{ready} == 1 && $clset->{"ready.op"} eq "not"
      && $clset->{"choice.op"} eq "or";
  my $schema = normalize_schema("int*");
  die "required schema normalization failed\n"
    unless $schema->[0] eq "int" && $schema->[1]{req} == 1;
  eval { normalize_schema({bad => 1}) };
  die "invalid schema was accepted\n" unless $@;
'
