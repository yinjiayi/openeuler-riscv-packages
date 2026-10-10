#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-Next
rpm -q --whatprovides 'perl(File::Next)'
perl -MFile::Next -MFile::Temp=tempdir -e '
  die "unexpected File::Next version\n" unless $File::Next::VERSION eq "1.18";
  my $dir = tempdir(CLEANUP => 1);
  open my $out, ">", "$dir/sample" or die $!;
  print {$out} "RVA23\n";
  close $out or die $!;
  my $files = File::Next::files($dir);
  die "iterator missed file\n" unless $files->() eq "$dir/sample";
  die "iterator returned extra files\n" if defined $files->();
'
