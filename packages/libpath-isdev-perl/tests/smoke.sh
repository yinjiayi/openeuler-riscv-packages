#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Path-IsDev
rpm -q --whatprovides 'perl(Path::IsDev)'
perl -MPath::IsDev=is_dev -MFile::Temp=tempdir -e '
  die "unexpected version\n" unless $Path::IsDev::VERSION eq "1.001003";
  my $root = tempdir(CLEANUP => 1);
  open my $marker, ">", "$root/.devdir" or die $!;
  close $marker;
  die "development marker not recognized\n" unless is_dev($root);
'
