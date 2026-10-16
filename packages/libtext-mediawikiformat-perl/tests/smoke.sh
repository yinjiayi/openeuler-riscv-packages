#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-MediawikiFormat
rpm -q --whatprovides 'perl(Text::MediawikiFormat)'
rpm -q --whatprovides 'perl(Text::MediawikiFormat::Block)'
rpm -q --whatprovides 'perl(Text::MediawikiFormat::Blocks)'
perl -MText::MediawikiFormat=wikiformat -e '
  die "wrong Text::MediawikiFormat version\n"
    unless $Text::MediawikiFormat::VERSION eq "1.04";
  die "paragraph formatting changed\n"
    unless wikiformat("Hello world") eq "<p>Hello world</p>\n";
'
