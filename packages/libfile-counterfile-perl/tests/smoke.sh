#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-CounterFile
rpm -q --whatprovides 'perl(File::CounterFile)'
perl -MFile::CounterFile -MFile::Temp=tempdir -e '
  die "wrong File::CounterFile version\n"
    unless $File::CounterFile::VERSION eq "1.04";
  my $dir = tempdir(CLEANUP => 1);
  my $path = "$dir/counter";
  my $counter = File::CounterFile->new($path);
  die "first increment changed\n" unless $counter->inc == 1;
  die "second increment changed\n" unless $counter->inc == 2;
  die "decrement changed\n" unless $counter->dec == 1;
'
