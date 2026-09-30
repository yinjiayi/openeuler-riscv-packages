#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-ConfigDir
rpm -q --whatprovides 'perl(File::ConfigDir)'
test_dir="$(mktemp -d)"
trap 'rmdir -- "$test_dir"' EXIT
perl -MFile::ConfigDir=config_dirs -e '
  die "unexpected File::ConfigDir version\n"
    unless $File::ConfigDir::VERSION eq "0.021";
  my $dir = $ARGV[0];
  File::ConfigDir::_plug_dir_source(sub { $dir }, 1)
    or die "could not register configuration directory\n";
  my @dirs = config_dirs();
  grep { $_ eq $dir } @dirs
    or die "registered directory missing from config_dirs\n";
' "$test_dir"
