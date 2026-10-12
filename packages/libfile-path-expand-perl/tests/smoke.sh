#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-Path-Expand
rpm -q --whatprovides 'perl(File::Path::Expand)'
perl -MFile::Path::Expand=expand_filename -e '
  die "unexpected File::Path::Expand version\n" unless $File::Path::Expand::VERSION eq "1.02";
  local $ENV{HOME} = "/tmp";
  die "HOME expansion failed\n" unless expand_filename("~/example") eq "/tmp/example";
'
