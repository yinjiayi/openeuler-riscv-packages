#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-Zglob
rpm -q --whatprovides 'perl(File::Zglob)'
perl -MFile::Temp=tempdir -MFile::Zglob -e '
  die "unexpected File::Zglob version\n"
    unless $File::Zglob::VERSION eq "0.11";
  my $dir = tempdir(CLEANUP => 1);
  mkdir "$dir/sub" or die $!;
  open my $fh, ">", "$dir/sub/a.txt" or die $!;
  print {$fh} "fixture\n";
  close $fh or die $!;
  my @matches = zglob("$dir/**/*.txt");
  @matches == 1 && $matches[0] eq "$dir/sub/a.txt"
    or die "recursive glob did not find the installed fixture\n";
'
