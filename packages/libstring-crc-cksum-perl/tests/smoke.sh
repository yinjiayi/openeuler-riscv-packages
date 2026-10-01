#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-CRC-Cksum
rpm -q --whatprovides 'perl(String::CRC::Cksum)'
perl -MString::CRC::Cksum -e '
  die "unexpected version\n" unless $String::CRC::Cksum::VERSION eq "0.91";
  my ($crc, $size) = String::CRC::Cksum::cksum("abc");
  die "known-vector mismatch\n" unless $crc == 1219131554 && $size == 3;
  my $stream = String::CRC::Cksum->new;
  $stream->add("a");
  $stream->add("bc");
  my ($stream_crc, $stream_size) = $stream->result;
  die "streaming mismatch\n"
    unless $stream_crc == $crc && $stream_size == $size;
'
