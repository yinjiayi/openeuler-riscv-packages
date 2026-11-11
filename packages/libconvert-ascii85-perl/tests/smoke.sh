#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-convert-ascii85
rpm -q --whatprovides 'perl(Convert::Ascii85)'
perl -MConvert::Ascii85=ascii85_encode,ascii85_decode -e '
  die "unexpected Convert::Ascii85 version\n" unless $Convert::Ascii85::VERSION eq "0.01";
  die "expected Ascii85 zero compression\n" unless ascii85_encode("\0" x 4, {}) eq "z";
  my $source = pack("C*", 0, 1, 2, 127, 128, 255, 44);
  die "binary round-trip failed\n" unless ascii85_decode(ascii85_encode($source, {})) eq $source;
'
