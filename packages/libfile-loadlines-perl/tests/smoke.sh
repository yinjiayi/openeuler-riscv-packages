#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-LoadLines
rpm -q --whatprovides 'perl(File::LoadLines)'
perl -MFile::Temp=tempdir -MFile::LoadLines=loadlines,loadblob -e '
  die "unexpected File::LoadLines version\n"
    unless $File::LoadLines::VERSION eq "1.047";
  my $dir = tempdir(CLEANUP => 1);
  my $path = "$dir/input.txt";
  open my $fh, ">:raw", $path or die $!;
  print {$fh} "alpha\r\nbeta\r\n";
  close $fh or die $!;
  my @lines = loadlines($path);
  @lines == 2 && $lines[0] eq "alpha" && $lines[1] eq "beta"
    or die "decoded lines mismatch\n";
  loadblob($path) eq "alpha\r\nbeta\r\n"
    or die "raw blob mismatch\n";
'
