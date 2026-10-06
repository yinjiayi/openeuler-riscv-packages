#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-FindLib
rpm -q --whatprovides 'perl(File::FindLib)'
perl -MFile::Temp=tempdir -e '
  require File::FindLib;
  die "unexpected File::FindLib version\n"
    unless $File::FindLib::VERSION eq "0.001004";
  my $root = tempdir(CLEANUP => 1);
  mkdir "$root/lib" or die $!;
  mkdir "$root/bin" or die $!;
  mkdir "$root/bin/deep" or die $!;
  open my $script, ">", "$root/bin/deep/run.pl" or die $!;
  print {$script} "1;\n";
  close $script or die $!;
  open my $module, ">", "$root/lib/FindLibSmoke.pm" or die $!;
  print {$module} "package FindLibSmoke; our \$VALUE = 42; 1;\n";
  close $module or die $!;
  my $found = File::FindLib::LookUp(
    -from => "$root/bin/deep/run.pl", -upto => "lib", -add => "lib"
  );
  $found eq "$root/lib" or die "wrong ancestor library path\n";
  require FindLibSmoke;
  $FindLibSmoke::VALUE == 42 or die "module was not loaded\n";
'
