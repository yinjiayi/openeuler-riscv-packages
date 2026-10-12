#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-Format
perl -MText::Format -e '
  die "unexpected version\n" unless $Text::Format::VERSION eq "0.63";
  my $formatter = Text::Format->new({
    columns => 10, firstIndent => 0, bodyIndent => 0
  });
  die "word wrap mismatch\n"
    unless $formatter->format("alpha beta gamma") eq "alpha beta\ngamma\n";
'
