#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-Copy-Link
rpm -q --whatprovides 'perl(File::Copy::Link)'
rpm -q --whatprovides 'perl(File::Spec::Link)'
perl -MFile::Temp=tempdir -MFile::Copy::Link -MFile::Spec::Link -e '
  die "unexpected File::Copy::Link version\n"
    unless $File::Copy::Link::VERSION eq "0.200";
  my $dir = tempdir(CLEANUP => 1);
  my $src = "$dir/source.txt";
  my $link = "$dir/link.txt";
  open my $fh, ">", $src or die $!;
  print {$fh} "fixture\n";
  close $fh or die $!;
  symlink "source.txt", $link or die $!;
  File::Spec::Link->linked($link) eq $src
    or die "linked target mismatch\n";
  system("copylink", $link) == 0 or die "copylink command failed\n";
  -l $link and die "symbolic link was not replaced\n";
  open my $copy, "<", $link or die $!;
  my $text = <$copy>;
  close $copy or die $!;
  $text eq "fixture\n" or die "replacement contents mismatch\n";
'
