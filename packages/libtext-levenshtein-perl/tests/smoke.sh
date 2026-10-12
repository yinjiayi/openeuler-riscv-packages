#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-Levenshtein
rpm -q --whatprovides 'perl(Text::Levenshtein)'
perl -MText::Levenshtein=distance -e '
  die "unexpected Text::Levenshtein version\n"
    unless $Text::Levenshtein::VERSION eq "0.15";
  die "edit distance mismatch\n"
    unless distance("kitten", "sitting") == 3;
'
