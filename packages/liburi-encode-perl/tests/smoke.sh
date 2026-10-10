#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-URI-Encode
rpm -q --whatprovides 'perl(URI::Encode)'
perl -MURI::Encode=uri_encode,uri_decode -e '
  die "wrong URI::Encode version\n" unless $URI::Encode::VERSION eq "1.1.1";
  die "percent encoding failed\n" unless uri_encode("a b") eq "a%20b";
  die "percent decoding failed\n" unless uri_decode("a%20b") eq "a b";
  my $encoder = URI::Encode->new({encode_reserved => 1});
  die "reserved-character encoding failed\n"
    unless $encoder->encode("a/b") eq "a%2Fb";
'
