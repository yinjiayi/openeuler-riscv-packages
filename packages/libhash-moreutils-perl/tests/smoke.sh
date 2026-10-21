#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Hash-MoreUtils
rpm -q --whatprovides 'perl(Hash::MoreUtils)'
perl -MHash::MoreUtils=slice,slice_def,slice_exists -e '
  die "unexpected version\n" unless $Hash::MoreUtils::VERSION eq "0.06";
  my %source = (a => 1, b => undef);
  my %selected = slice(\%source, qw(a c));
  die "slice failed\n" unless $selected{a} == 1 && exists $selected{c};
  my %defined = slice_def(\%source, qw(a b));
  die "defined slice failed\n" unless keys(%defined) == 1 && $defined{a} == 1;
  my %existing = slice_exists(\%source, qw(a c));
  die "existing slice failed\n" unless keys(%existing) == 1 && exists $existing{a};
'
