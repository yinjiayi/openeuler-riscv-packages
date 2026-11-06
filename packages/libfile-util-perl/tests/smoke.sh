#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-Util
rpm -q --whatprovides 'perl(File::Util)'
perl -MFile::Util -MFile::Temp=tempdir -e '
  die "wrong File::Util version\n" unless $File::Util::VERSION eq "4.201720";
  my $dir = tempdir(CLEANUP => 1);
  my $path = "$dir/probe.txt";
  my $files = File::Util->new();
  $files->write_file($path => "hello\n");
  die "installed file round-trip failed\n"
    unless $files->load_file($path) eq "hello\n";
'
