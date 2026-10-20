#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-TabularDisplay
rpm -q --whatprovides 'perl(Text::TabularDisplay)'
perl -MText::TabularDisplay -e '
  die "unexpected Text::TabularDisplay version\n"
    unless $Text::TabularDisplay::VERSION eq "1.38";
  my $table = Text::TabularDisplay->new("Name", "Age");
  $table->add("Ada", 36);
  my $rendered = $table->render;
  die "table rendering mismatch\n"
    unless $rendered =~ /\| Name\s+\| Age\s+\|/ &&
           $rendered =~ /\| Ada\s+\| 36\s+\|/;
'
