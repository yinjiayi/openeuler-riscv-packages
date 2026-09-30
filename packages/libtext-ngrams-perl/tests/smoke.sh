#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-Ngrams
rpm -q --whatprovides 'perl(Text::Ngrams)'
perl -MText::Ngrams -e '
  die "unexpected Text::Ngrams version\n"
    unless $Text::Ngrams::VERSION eq "2.007";
  my $analyzer = Text::Ngrams->new(windowsize => 2, type => "byte");
  $analyzer->process_text("abab");
  my %ngrams = $analyzer->get_ngrams(n => 2);
  $ngrams{"a b"} == 2 && $ngrams{"b a"} == 1
    or die "wrong two-gram counts\n";
'
command -v ngrams.pl
output=$(printf 'abab' | ngrams.pl --n=2 --type=byte --orderby=ngram)
[[ "$output" == *"2-GRAMS"* ]]
