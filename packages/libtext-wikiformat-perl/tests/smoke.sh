#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-WikiFormat
rpm -q --whatprovides 'perl(Text::WikiFormat)'
perl -MText::WikiFormat -e '
  die "unexpected Text::WikiFormat version\n"
    unless $Text::WikiFormat::VERSION eq "0.81";
  die "plain Wiki paragraph formatting mismatch\n"
    unless Text::WikiFormat::format("hello") eq "<p>hello</p>\n";
'
