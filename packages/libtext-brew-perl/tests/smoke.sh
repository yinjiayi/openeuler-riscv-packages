#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-Brew
rpm -q --whatprovides 'perl(Text::Brew)'
perl -MText::Brew=distance -e '
  die "unexpected Text::Brew version\n"
    unless $Text::Brew::VERSION eq "0.02";
  my ($distance, $edits) = distance("abcd", "bcd");
  die "Brew distance or edit sequence mismatch\n"
    unless $distance == 1
       && join(",", @$edits) eq "INITIAL,DEL,MATCH,MATCH,MATCH";
'
