#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-CountLines
rpm -q --whatprovides 'perl(File::CountLines)'
perl -MFile::Temp=tempdir -MFile::CountLines=count_lines -e '
  die "unexpected File::CountLines version\n"
    unless $File::CountLines::VERSION eq "0.0.3";
  my $dir = tempdir(CLEANUP => 1);
  my $path = "$dir/input.txt";
  open my $fh, ">", $path or die $!;
  print {$fh} "alpha\r\nbeta\r\n";
  close $fh or die $!;
  count_lines($path) == 2 or die "native line count mismatch\n";
  count_lines($path, style => "crlf") == 2
    or die "CRLF line count mismatch\n";
'
