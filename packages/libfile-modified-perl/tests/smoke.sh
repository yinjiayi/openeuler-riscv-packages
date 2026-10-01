#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-Modified
rpm -q --whatprovides 'perl(File::Modified)'
perl -MFile::Modified -e '
  die "unexpected File::Modified version\n" unless $File::Modified::VERSION eq "0.10";
  my $signature = File::Modified->new(method => "mtime", files => ["/etc/passwd"]);
  die "unchanged file reported modified\n" if $signature->changed();
'
