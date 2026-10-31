#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-RewriteRules
rpm -q --whatprovides 'perl(Text::RewriteRules)'
perl -MText::RewriteRules -e '
  die "unexpected Text::RewriteRules version\n"
    unless $Text::RewriteRules::VERSION eq "0.25";
RULES swap
foo==>bar
ENDRULES
  die "rewrite mismatch\n" unless swap("food") eq "bard";
'

compiled="$(printf 'use Text::RewriteRules;\nRULES swap\nfoo==>bar\nENDRULES\nprint swap("food"), "\\n";\n' | textrr | perl)"
test "$compiled" = bard
