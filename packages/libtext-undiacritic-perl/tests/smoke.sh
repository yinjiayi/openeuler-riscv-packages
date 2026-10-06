#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-Undiacritic
rpm -q --whatprovides 'perl(Text::Undiacritic)'
perl -MText::Undiacritic=undiacritic -e '
  die "unexpected Text::Undiacritic version\n"
    unless $Text::Undiacritic::VERSION eq "0.07";
  undiacritic(chr(0x00E4)) eq "a"
    or die "precomposed diacritic mismatch\n";
  undiacritic("o" . chr(0x0308)) eq "o"
    or die "combining diacritic mismatch\n";
'
