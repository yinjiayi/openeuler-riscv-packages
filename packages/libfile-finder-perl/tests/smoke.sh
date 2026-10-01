#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-Finder
rpm -q --whatprovides 'perl(File::Finder)'
rpm -q --whatprovides 'perl(File::Finder::Steps)'
perl -MFile::Finder -MFile::Finder::Steps -MFile::Temp=tempdir -e '
  die "unexpected File::Finder version\n"
    unless $File::Finder::VERSION eq "1.01";
  my $dir = tempdir(CLEANUP => 1);
  mkdir "$dir/sub" or die $!;
  open my $fh, ">", "$dir/one.txt" or die $!;
  print {$fh} "fixture\n";
  close $fh or die $!;
  open my $other, ">", "$dir/sub/two.log" or die $!;
  print {$other} "fixture\n";
  close $other or die $!;
  my @matches = File::Finder->type("f")->name("*.txt")->in($dir);
  @matches == 1 && $matches[0] eq "$dir/one.txt"
    or die "installed finder returned unexpected paths\n";
'
