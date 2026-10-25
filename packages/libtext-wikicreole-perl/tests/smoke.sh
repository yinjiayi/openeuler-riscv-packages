#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-WikiCreole
rpm -q --whatprovides 'perl(Text::WikiCreole)'
perl -MText::WikiCreole -e '
  die "unexpected Text::WikiCreole version\n"
    unless $Text::WikiCreole::VERSION eq "0.07";
  die "Wiki Creole paragraph conversion mismatch\n"
    unless creole_parse("hello") eq "<p>hello</p>\n\n";
'
