#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-Patch
rpm -q --whatprovides 'perl(Text::Patch)'
perl -MText::Patch=patch -e '
  die "unexpected Text::Patch version\n" unless $Text::Patch::VERSION eq "1.8";
  my $source = "one\ntwo\n";
  my $diff = "@@ -1,2 +1,2 @@\n one\n-two\n+TWO\n";
  my $result = patch($source, $diff, STYLE => "Unified");
  die "unified patch output mismatch\n" unless $result eq "one\nTWO\n";
  die "source text changed\n" unless $source eq "one\ntwo\n";
'
