#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-CSV-Unicode
rpm -q --whatprovides 'perl(Text::CSV::Unicode)'
rpm -q --whatprovides 'perl(Text::CSV)'
perl -MText::CSV::Unicode -e '
  use utf8;
  die "unexpected version\n" unless $Text::CSV::Unicode::VERSION eq "0.400";
  my $csv = Text::CSV::Unicode->new();
  die "combine failed\n" unless $csv->combine("caf\xe9", "\x{4e16}\x{754c}");
  my $record = $csv->string;
  my $parsed = Text::CSV::Unicode->new();
  die "parse failed\n" unless $parsed->parse($record);
  my @fields = $parsed->fields;
  die "Unicode roundtrip failed\n"
    unless @fields == 2 && $fields[0] eq "caf\xe9" && $fields[1] eq "\x{4e16}\x{754c}";
  die "control character accepted\n" if $csv->combine("a\nb");
'
