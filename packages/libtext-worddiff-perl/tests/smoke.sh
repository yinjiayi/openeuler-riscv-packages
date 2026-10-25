#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-WordDiff
rpm -q --whatprovides 'perl(Text::WordDiff)'
perl -MText::WordDiff -MText::WordDiff::HTML -MText::WordDiff::ANSIColor -MText::WordDiff::HTMLTwoLines -e '
  die "unexpected Text::WordDiff version\n"
    unless $Text::WordDiff::VERSION eq "0.09";
  my ($old, $new) = ("red blue", "red green");
  my $html = word_diff(\$old, \$new, { STYLE => "HTML" });
  index($html, "<del>blue</del><ins>green</ins>") >= 0
    or die "word-oriented HTML diff mismatch\n";
'
