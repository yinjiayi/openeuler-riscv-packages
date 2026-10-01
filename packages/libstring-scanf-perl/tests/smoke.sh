#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-Scanf
rpm -q --whatprovides 'perl(String::Scanf)'
perl -MString::Scanf -e '
  die "unexpected version\n" unless $String::Scanf::VERSION eq "2.1";
  my ($number, $word) = sscanf("%d %3s", "42 abc");
  die "function parse failed\n" unless $number == 42 && $word eq "abc";
  my $parser = String::Scanf->new("%x:%o");
  my ($hex, $oct) = $parser->sscanf("ff:17");
  die "object parse failed\n" unless $hex == 255 && $oct == 15;
'
