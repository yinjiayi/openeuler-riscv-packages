#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-Lorem
rpm -q --whatprovides 'perl(Text::Lorem)'
perl -MText::Lorem -e '
  die "unexpected Text::Lorem version\n"
    unless $Text::Lorem::VERSION eq "0.34";
  my $generator = Text::Lorem->new;
  my @words = $generator->words(3);
  @words == 3 or die "wrong word count\n";
  my @sentences = $generator->sentences(2);
  @sentences == 2 or die "wrong sentence count\n";
  my @paragraphs = $generator->paragraphs(2);
  @paragraphs == 2 or die "wrong paragraph count\n";
'
command -v lorem
test "$(lorem -w 3 | wc -w | tr -d ' ')" = 3
