#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-Iconv
rpm -q --whatprovides 'perl(Text::Iconv)'
perl -MText::Iconv -e '
  die "unexpected version\n" unless $Text::Iconv::VERSION eq "1.7";
  my $to_utf8 = Text::Iconv->new("ISO-8859-1", "UTF-8");
  my $from_utf8 = Text::Iconv->new("UTF-8", "ISO-8859-1");
  my $latin1 = "Sch\xf6n";
  my $utf8 = $to_utf8->convert($latin1);
  die "forward conversion failed\n" unless $utf8 eq "Sch\xc3\xb6n";
  die "roundtrip conversion failed\n" unless $from_utf8->convert($utf8) eq $latin1;
'
