#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-URI-ToDisk
rpm -q --whatprovides 'perl(URI::ToDisk)'
perl -MURI::ToDisk -e '
  die "unexpected URI::ToDisk version\n" unless $URI::ToDisk::VERSION eq "1.12";
  my $base = URI::ToDisk->new("/probe", "http://example.org/base");
  die "base path mismatch\n" unless $base->path eq "/probe";
  my $child = $base->catfile("docs", "readme.txt");
  die "child path mismatch\n" unless $child->path eq "/probe/docs/readme.txt";
  die "child URI mismatch\n" unless $child->uri eq "http://example.org/base/docs/readme.txt";
  die "base mutated\n" unless $base->path eq "/probe";
'
