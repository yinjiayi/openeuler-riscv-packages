#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Hash-Util-FieldHash-Compat
rpm -q --whatprovides 'perl(Hash::Util::FieldHash::Compat)'
perl -MHash::Util::FieldHash::Compat=fieldhash -e '
  die "unexpected compat version\n"
    unless $Hash::Util::FieldHash::Compat::VERSION eq "0.11";
  die "native fieldhash provider not selected\n"
    unless Hash::Util::FieldHash::Compat::REAL_FIELDHASH();
  my %values;
  fieldhash %values;
  my $key = bless {}, "CompatSmokeKey";
  $values{$key} = "present";
  die "fieldhash lookup mismatch\n"
    unless $values{$key} eq "present";
'
