#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-Typography
rpm -q --whatprovides 'perl(Text::Typography)'
perl -MText::Typography=typography -e '
  die "unexpected Text::Typography version\n"
    unless $Text::Typography::VERSION eq "0.01";
  die "ellipsis conversion mismatch\n"
    unless typography("Wait...") eq "Wait&#8230;";
  die "dash conversion mismatch\n"
    unless typography("a -- b") eq "a &#8212; b";
  die "code-block preservation mismatch\n"
    unless typography("<code>Wait...</code>") eq "<code>Wait...</code>";
'
