#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-ASCIITable
perl -MText::ASCIITable -MText::ASCIITable::Wrap -e '
  die "unexpected version\n" unless $Text::ASCIITable::VERSION eq "0.22";
  my $table = Text::ASCIITable->new;
  $table->setCols(qw(Name Value));
  $table->addRow(qw(alpha beta));
  my $rendered = $table->draw;
  die "table render mismatch\n"
    unless $rendered =~ /\| alpha \| beta  \|/;
'
