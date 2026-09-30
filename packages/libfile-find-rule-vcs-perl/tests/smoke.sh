#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-Find-Rule-VCS
rpm -q --whatprovides 'perl(File::Find::Rule::VCS)'
perl -MFile::Temp=tempdir -MFile::Path=make_path -MFile::Find::Rule -MFile::Find::Rule::VCS -e '
  die "unexpected File::Find::Rule::VCS version\n"
    unless $File::Find::Rule::VCS::VERSION eq "1.09";
  my $dir = tempdir(CLEANUP => 1);
  make_path("$dir/.git");
  for my $path ("$dir/.git/config", "$dir/keep.txt") {
    open my $fh, ">", $path or die $!;
    print {$fh} "fixture\n";
    close $fh or die $!;
  }
  my @all = File::Find::Rule->file->in($dir);
  my @kept = File::Find::Rule->ignore_git->file->in($dir);
  @all == 2 or die "baseline search did not find both files\n";
  @kept == 1 && $kept[0] eq "$dir/keep.txt"
    or die "Git metadata was not excluded\n";
'
