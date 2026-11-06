#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Path-Iter
rpm -q --whatprovides 'perl(Path::Iter)'
perl -MPath::Iter -MFile::Temp=tempdir -e '
  die "unexpected version\n" unless $Path::Iter::VERSION == 0.2;
  my $root = tempdir(CLEANUP => 1);
  mkdir "$root/child" or die $!;
  open my $created, ">", "$root/child/payload" or die $!;
  close $created;
  my $next = Path::Iter::get_iterator($root);
  my %seen;
  while (my $path = $next->()) { $seen{$path} = 1 }
  die "iteration missed files\n" unless
    $seen{$root} && $seen{"$root/child"} && $seen{"$root/child/payload"};
'
