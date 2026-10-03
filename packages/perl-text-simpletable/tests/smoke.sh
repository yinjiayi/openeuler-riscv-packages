#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-SimpleTable
rpm -q --whatprovides 'perl(Text::SimpleTable)'
perl -MUnicode::GCString -MMIME::Charset -MText::SimpleTable -e '
  use utf8;
  die "unexpected Text::SimpleTable version\n"
    unless $Text::SimpleTable::VERSION eq "2.07";
  my $ascii = Text::SimpleTable->new(3, 3);
  $ascii->row("foo", "bar");
  die "ASCII table mismatch\n"
    unless $ascii->draw eq ".-----+-----.\n| foo | bar |\n\x27-----+-----\x27\n";
  my $wide = Text::SimpleTable->new(10);
  $wide->row("あいうえお");
  my $rendered = $wide->draw;
  die "Unicode table mismatch\n" unless $rendered =~ /あいうえお/;
'
