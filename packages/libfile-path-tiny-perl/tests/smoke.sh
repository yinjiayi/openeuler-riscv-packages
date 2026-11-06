#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-Path-Tiny
rpm -q --whatprovides 'perl(File::Path::Tiny)'
perl -MFile::Path::Tiny -MFile::Temp=tempdir -e '
  die "unexpected version\n" unless $File::Path::Tiny::VERSION eq "1.0";
  my $root = tempdir(CLEANUP => 1);
  my $path = "$root/alpha/beta";
  die "mkdir failed\n" unless File::Path::Tiny::mk($path);
  die "missing directory\n" unless -d $path;
  die "remove failed\n" unless File::Path::Tiny::rm("$root/alpha");
  die "directory remains\n" if -e "$root/alpha";
'
