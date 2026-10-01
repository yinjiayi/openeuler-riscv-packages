#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-CheckTree
rpm -q --whatprovides 'perl(File::CheckTree)'
perl -MFile::CheckTree=validate -e '
  die "unexpected File::CheckTree version\n" unless $File::CheckTree::VERSION eq "4.42";
  my $warnings = validate("/etc/passwd -f || die\n");
  die "valid file produced a warning\n" unless $warnings == 0;
'
