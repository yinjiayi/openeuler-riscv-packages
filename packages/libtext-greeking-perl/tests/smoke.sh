#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-Greeking
rpm -q --whatprovides 'perl(Text::Greeking)'
perl -MText::Greeking -e '
  die "unexpected Text::Greeking version\n"
    unless $Text::Greeking::VERSION eq "0.15";
  my $generator = Text::Greeking->new;
  $generator->add_source("alpha beta gamma");
  $generator->paragraphs(1, 1);
  $generator->sentences(1, 1);
  $generator->words(3, 3);
  my $output = $generator->generate;
  $output =~ /\A(?:Alpha|Beta|Gamma)(?:[,;:]| --)? (?:alpha|beta|gamma)(?:[,;:]| --)? (?:alpha|beta|gamma)[.?!]\n\n\z/
    or die "unexpected generated text: $output\n";
'
