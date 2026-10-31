#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-Reform
rpm -q --whatprovides 'perl(Text::Reform)'
perl -MText::Reform=form -e '
  die "unexpected Text::Reform version\n"
    unless $Text::Reform::VERSION eq "1.20";
  form("<<<<<", "alpha") eq "alpha\n"
    or die "text formatting mismatch\n";
'
