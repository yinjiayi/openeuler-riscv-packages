#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-Share
rpm -q --whatprovides 'perl(File::Share)'
perl -MFile::Share -MFile::Temp=tempdir -MFile::Path=make_path -e '
  die "unexpected File::Share version\n"
    unless $File::Share::VERSION eq "0.27";
  my $dir = tempdir(CLEANUP => 1);
  make_path("$dir/lib/Foo", "$dir/share");
  open my $module, ">", "$dir/lib/Foo/Bar.pm" or die $!;
  print {$module} "package Foo::Bar; 1;\n";
  close $module or die $!;
  open my $file, ">", "$dir/share/data.txt" or die $!;
  print {$file} "fixture\n";
  close $file or die $!;
  unshift @INC, "$dir/lib";
  require Foo::Bar;
  my $path = File::Share::dist_file("Foo-Bar", "data.txt");
  open my $found, "<", $path or die "$path: $!";
  my $contents = <$found>;
  close $found or die $!;
  $contents eq "fixture\n" or die "local share lookup mismatch\n";
'
