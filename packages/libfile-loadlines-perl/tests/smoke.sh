#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-LoadLines
rpm -q --whatprovides 'perl(File::LoadLines)'
perl -MFile::LoadLines -e '
  die "unexpected File::LoadLines version\n" unless $File::LoadLines::VERSION eq "1.047";
  my @lines = loadlines("data:text/plain;base64,YWxwaGEKYmV0YQo=");
  die "base64 data URL line loading failed\n"
    unless @lines == 2 && $lines[0] eq "alpha" && $lines[1] eq "beta";
'
