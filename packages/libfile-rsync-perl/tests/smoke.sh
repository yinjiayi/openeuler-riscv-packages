#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-File-Rsync
rpm -q --whatprovides 'perl(File::Rsync)'
perl -MFile::Rsync -e '
  die "unexpected version\n" unless $File::Rsync::VERSION eq "0.49";
  my $r = File::Rsync->new(archive => 1) or die "constructor failed\n";
  my $cmd = $r->getcmd(src => "source", dest => "destination");
  die "argument construction mismatch\n"
    unless join(" ", @$cmd) eq "rsync --archive source destination";
'
