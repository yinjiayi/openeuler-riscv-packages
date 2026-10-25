#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-Capitalize
rpm -q --whatprovides 'perl(Text::Capitalize)'
perl -MText::Capitalize -e '
  die "unexpected Text::Capitalize version\n"
    unless $Text::Capitalize::VERSION eq "1.5";
  my $title = capitalize_title("the lord of the rings");
  $title eq "The Lord of the Rings"
    or die "installed title capitalization mismatch: $title\n";
'
