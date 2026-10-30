#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-CSV_XS
rpm -q --whatprovides 'perl(Text::CSV_XS)'
perl -MText::CSV_XS -e '
  die "unexpected version\n" unless $Text::CSV_XS::VERSION eq "1.64";
  my $csv = Text::CSV_XS->new({ binary => 1 })
    or die "CSV parser unavailable\n";
  $csv->parse(q{"a,b",c}) or die "CSV parse failed\n";
  my @fields = $csv->fields;
  die "quoted field mismatch\n"
    unless @fields == 2 && $fields[0] eq "a,b" && $fields[1] eq "c";
  $csv->combine("x,y", "z") or die "CSV compose failed\n";
  die "CSV serialization mismatch\n"
    unless $csv->string eq q{"x,y",z};
'
