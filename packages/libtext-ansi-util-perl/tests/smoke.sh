#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-ANSI-Util
rpm -q --whatprovides 'perl(Text::ANSI::Util)'
rpm -q --whatprovides 'perl(Text::ANSI::BaseUtil)'
perl -MText::ANSI::Util=ta_strip,ta_length -e '
  die "unexpected Text::ANSI::Util version\n"
    unless $Text::ANSI::Util::VERSION eq "0.234";
  my $colored = "\e[31mhi\e[0m";
  die "ANSI strip or visible-length result mismatch\n"
    unless ta_strip($colored) eq "hi" && ta_length($colored) == 2;
'
