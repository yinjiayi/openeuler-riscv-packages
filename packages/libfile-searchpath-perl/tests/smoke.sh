#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-SearchPath
rpm -q --whatprovides 'perl(File::SearchPath)'
perl -MFile::SearchPath=searchpath -e '
  die "unexpected File::SearchPath version\n" unless $File::SearchPath::VERSION eq "0.07";
  my $path = searchpath("sh", env => "PATH", exe => 1);
  die "shell executable not found\n" unless defined($path) && -f $path && -x $path;
'
