#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-Levenshtein-Damerau
rpm -q --whatprovides 'perl(Text::Levenshtein::Damerau)'
rpm -q --whatprovides 'perl(Text::Levenshtein::Damerau::PP)'
perl -MText::Levenshtein::Damerau=edistance -MText::Levenshtein::Damerau::PP -e '
  die "unexpected module versions\n"
    unless $Text::Levenshtein::Damerau::VERSION eq "0.41"
       && $Text::Levenshtein::Damerau::PP::VERSION eq "0.25";
  die "transposition distance mismatch\n"
    unless edistance("Niel", "Neil") == 1;
  die "object distance mismatch\n"
    unless Text::Levenshtein::Damerau->new("four")->dld("fuor") == 1;
'
