#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-Monitor
rpm -q --whatprovides 'perl(File::Monitor)'
perl -MFile::Monitor -MFile::Temp=tempdir -e '
  die "wrong File::Monitor version\n"
    unless $File::Monitor::VERSION eq "1.00";
  my $dir = tempdir(CLEANUP => 1);
  my $path = "$dir/watched";
  open my $fh, ">", $path or die $!;
  print {$fh} "a";
  close $fh;
  my $monitor = File::Monitor->new();
  $monitor->watch($path);
  die "initial scan reported a change\n" if $monitor->scan;
  open $fh, ">", $path or die $!;
  print {$fh} "abcdef";
  close $fh;
  my @changes = $monitor->scan;
  die "file size change was not detected\n" unless @changes;
'
