#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Convert-BinHex
rpm -q --whatprovides 'perl(Convert::BinHex)'
command -v binhex.pl
command -v debinhex.pl
perl -c "$(command -v binhex.pl)"
perl -c "$(command -v debinhex.pl)"
perl -MConvert::BinHex=binhex_crc -e '
  die "unexpected Convert::BinHex version\n" unless $Convert::BinHex::VERSION eq "1.125";
  my $data = "U1SBdxdMHpA2wlW3TOgUHXZ00jvHnkyU/ndXnr9RMElXdQXUAGYrPpf4F8jO";
  die "BinHex CRC mismatch\n" unless binhex_crc($data) == 35360;
'
