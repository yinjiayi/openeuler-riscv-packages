#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-Header
rpm -q --whatprovides 'perl(Text::Header)'
perl -MText::Header -e '
  die "unexpected version\n" unless $Text::Header::VERSION eq "1.03";
  my @lines = header(content_type => "text/plain");
  die "header mismatch\n" unless @lines == 1 && $lines[0] eq "Content-Type: text/plain\n";
  my @parts = unheader(@lines);
  die "parse mismatch\n"
    unless @parts == 2 && $parts[0] eq "content_type" && $parts[1] eq "text/plain";
'
