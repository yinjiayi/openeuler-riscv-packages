#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-sprintfn
rpm -q --whatprovides 'perl(Text::sprintfn)'
perl -MText::sprintfn=sprintfn -e '
  die "unexpected Text::sprintfn version\n"
    unless $Text::sprintfn::VERSION eq "0.090";
  die "named parameter formatting mismatch\n"
    unless sprintfn("Hello %(name)s", {name => "Ada"}) eq "Hello Ada";
'
