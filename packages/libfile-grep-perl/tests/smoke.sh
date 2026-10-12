#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-Grep
rpm -q --whatprovides 'perl(File::Grep)'
perl -MFile::Temp=tempdir -MFile::Grep=fgrep,fmap,fdo -e '
  die "unexpected File::Grep version\n"
    unless $File::Grep::VERSION eq "0.02";
  my $dir = tempdir(CLEANUP => 1);
  my $path = "$dir/smoke.txt";
  open my $out, ">", $path or die $!;
  print {$out} "Bob\nAlice\nBob\n";
  close $out or die $!;
  my $count = fgrep { /Bob/ } $path;
  $count == 2 or die "fgrep count mismatch\n";
  my @mapped = fmap { lc } $path;
  @mapped == 3 && $mapped[0] eq "bob\n" && $mapped[2] eq "bob\n"
    or die "fmap result mismatch\n";
  my $seen = 0;
  fdo { $seen++ } $path;
  $seen == 3 or die "fdo count mismatch\n";
'
