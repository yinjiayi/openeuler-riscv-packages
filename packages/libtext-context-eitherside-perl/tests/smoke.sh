#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-Context-EitherSide
rpm -q --whatprovides 'perl(Text::Context::EitherSide)'
perl -MText::Context::EitherSide=get_context -e '
  die "unexpected Text::Context::EitherSide version\n"
    unless $Text::Context::EitherSide::VERSION eq "1.4";
  my $text = "The quick brown fox jumped over the lazy dog";
  die "context extraction mismatch\n"
    unless get_context(2, $text, "fox") eq
      "... quick brown fox jumped over ...";
'
