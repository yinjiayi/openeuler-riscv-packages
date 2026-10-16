#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-WagnerFischer
rpm -q --whatprovides 'perl(Text::WagnerFischer)'
perl -MText::WagnerFischer=distance -e '
  die "unexpected version\n" unless $Text::WagnerFischer::VERSION eq "0.04";
  die "edit distance\n" unless distance("foo", "four") == 2;
  die "weighted distance\n" unless distance([0,1,2], "foo", "four") == 3;
  my @distances = distance("foo", "four", "foo", "bar");
  die "candidate distances\n" unless join(",", @distances) eq "2,0,3";
'
