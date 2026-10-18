#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-ShareDir-Tiny
rpm -q --whatprovides 'perl(File::ShareDir::Tiny)'
perl -MFile::Temp=tempdir -MFile::Path=make_path -MFile::ShareDir::Tiny=:ALL -e '
  die "unexpected File::ShareDir::Tiny version\n"
    unless $File::ShareDir::Tiny::VERSION eq "0.001";
  my $root = tempdir(CLEANUP => 1);
  my $dist = "$root/auto/share/dist/Smoke-Dist";
  my $module = "$root/auto/share/module/Smoke-Module";
  make_path($dist, $module);
  for my $path ("$dist/dist.txt", "$module/module.txt") {
    open my $out, ">", $path or die $!;
    print {$out} "smoke\n";
    close $out or die $!;
  }
  local @INC = ($root, @INC);
  dist_dir("Smoke-Dist") eq $dist or die "wrong dist dir\n";
  module_dir("Smoke::Module") eq $module or die "wrong module dir\n";
  dist_file("Smoke-Dist", "dist.txt") eq "$dist/dist.txt"
    or die "wrong dist file\n";
  module_file("Smoke::Module", "module.txt") eq "$module/module.txt"
    or die "wrong module file\n";
'
