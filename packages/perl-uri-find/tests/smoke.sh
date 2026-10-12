#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-URI-Find
rpm -q --whatprovides 'perl(URI::Find)'
perl -MURI::Find -MURI::Find::Schemeless -e '
  die "unexpected version\n" unless $URI::Find::VERSION eq "20160806";
  my $text = "See https://example.org/path for details";
  my @found;
  my $finder = URI::Find->new(sub {
    my ($uri, $original) = @_;
    push @found, "$uri";
    return $original;
  });
  my $count = $finder->find(\$text);
  die "URI discovery mismatch\n"
    unless $count == 1 && @found == 1
      && $found[0] eq "https://example.org/path"
      && $text eq "See https://example.org/path for details";
'
printf 'https://example.org/path\n' | urifind | grep -Fx 'https://example.org/path'
