#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Text-xSV
perl -MText::xSV -e '
  die "wrong version\n" unless $Text::xSV::VERSION == 0.21;
  my $data = "name,value\nalpha,\"x,y\"\n";
  open my $fh, "<", \$data or die $!;
  my $csv = Text::xSV->new(fh => $fh);
  $csv->bind_header;
  $csv->get_row or die "missing row\n";
  my ($name, $value) = $csv->extract("name", "value");
  die "incorrect CSV parsing\n" unless $name eq "alpha" && $value eq "x,y";
'
