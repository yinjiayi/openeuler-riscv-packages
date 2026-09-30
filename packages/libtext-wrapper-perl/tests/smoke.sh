#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-Wrapper
rpm -q --whatprovides 'perl(Text::Wrapper)'
perl -MText::Wrapper -e '
  die "unexpected Text::Wrapper version\n"
    unless $Text::Wrapper::VERSION eq "1.05";
  my $wrapper = Text::Wrapper->new(columns => 8);
  $wrapper->wrap("alpha beta gamma") eq "alpha\nbeta\ngamma\n"
    or die "wrong wrapped output\n";
'
