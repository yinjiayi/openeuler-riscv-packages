#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-FormatTable
perl -MText::FormatTable -e '
  die "unexpected version\n" unless $Text::FormatTable::VERSION eq "1.03";
  my $table = Text::FormatTable->new("l l");
  $table->head("Name", "Value");
  $table->row("alpha", "beta");
  my $rendered = $table->render();
  die "table render mismatch\n"
    unless $rendered eq "Name  Value\nalpha beta \n";
'
