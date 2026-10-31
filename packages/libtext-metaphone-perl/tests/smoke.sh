#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-Metaphone
rpm -q --whatprovides 'perl(Text::Metaphone)'
perl -MText::Metaphone -e '
  die "unexpected version\n" unless $Text::Metaphone::VERSION eq "20160805";
  die "Schwern encoding\n" unless Metaphone("Schwern") eq "XWRN";
  die "Smith encoding\n" unless Metaphone("Smith") eq "SM0";
'
