#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-Trim
rpm -q --whatprovides 'perl(Text::Trim)'
perl -MText::Trim -e '
  die "unexpected Text::Trim version\n"
    unless $Text::Trim::VERSION eq "1.04";
  trim("  alpha beta  ") eq "alpha beta"
    or die "trim result mismatch\n";
  ltrim("  alpha  ") eq "alpha  "
    or die "ltrim result mismatch\n";
  rtrim("  alpha  ") eq "  alpha"
    or die "rtrim result mismatch\n";
'
