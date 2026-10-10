#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-FindIndent
rpm -q --whatprovides 'perl(Text::FindIndent)'
perl -MText::FindIndent -e '
  die "unexpected Text::FindIndent version\n"
    unless $Text::FindIndent::VERSION eq "0.12";
  my $text = "root\n    child\n        grandchild\n";
  die "space indentation detection failed\n"
    unless Text::FindIndent->parse($text) eq "s4";
'
