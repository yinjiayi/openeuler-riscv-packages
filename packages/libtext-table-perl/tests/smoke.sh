#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-Table
rpm -q --whatprovides 'perl(Text::Table)'
perl -MText::Table -e '
  die "unexpected Text::Table version\n" unless $Text::Table::VERSION eq "1.135";
  my $table = Text::Table->new("Name", "Age");
  $table->load(["Ada", 36]);
  my @lines = split /\n/, "$table";
  die "table rendering mismatch\n"
    unless @lines == 2 && $lines[0] =~ /Name\s+Age/ &&
           $lines[1] =~ /Ada\s+36/;
'
