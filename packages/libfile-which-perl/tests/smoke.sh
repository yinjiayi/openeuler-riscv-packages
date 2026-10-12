#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-Which
rpm -q --whatprovides 'perl(File::Which)'
perl -MFile::Which=which -e '
  die "unexpected File::Which version\n" unless $File::Which::VERSION eq "1.27";
  my $path = which("sh");
  die "shell executable not found\n" unless defined($path) && -f $path && -x $path;
'
