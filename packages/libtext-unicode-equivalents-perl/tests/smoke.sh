#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-Unicode-Equivalents
rpm -q --whatprovides 'perl(Text::Unicode::Equivalents)'
perl -MText::Unicode::Equivalents=all_strings -e '
  die "unexpected module version\n"
    unless $Text::Unicode::Equivalents::VERSION eq "0.05";
  my $forms = all_strings("\x{00e9}");
  my %seen = map { $_ => 1 } @$forms;
  die "missing canonical Unicode forms\n"
    unless $seen{"\x{00e9}"} && $seen{"e\x{0301}"};
'
