#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-Slurp-Tiny
rpm -q --whatprovides 'perl(File::Slurp::Tiny)'
perl -MFile::Temp=tempdir -MFile::Slurp::Tiny=read_file,read_lines,write_file,read_dir -e '
  die "unexpected File::Slurp::Tiny version\n"
    unless $File::Slurp::Tiny::VERSION eq "0.004";
  my $dir = tempdir(CLEANUP => 1);
  my $path = "$dir/smoke.txt";
  write_file($path, "alpha\nbeta\n");
  read_file($path) eq "alpha\nbeta\n" or die "read_file mismatch\n";
  my @lines = read_lines($path, chomp => 1);
  @lines == 2 && $lines[0] eq "alpha" && $lines[1] eq "beta"
    or die "read_lines mismatch\n";
  my @names = read_dir($dir);
  @names == 1 && $names[0] eq "smoke.txt"
    or die "read_dir mismatch\n";
'
