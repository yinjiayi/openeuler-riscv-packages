#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Hash-FieldHash
rpm -q --whatprovides 'perl(Hash::FieldHash)'
perl -MHash::FieldHash=:all -e '
  die "unexpected Hash::FieldHash version\n"
    unless $Hash::FieldHash::VERSION eq "0.15";
  fieldhash my %field;
  my $object = bless {}, "FieldHashSmoke";
  $field{$object} = 42;
  die "field lookup mismatch\n" unless $field{$object} == 42;
  undef $object;
  die "field was not released\n" unless keys(%field) == 0;
'
