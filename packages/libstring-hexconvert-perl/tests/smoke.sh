#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-HexConvert
rpm -q --whatprovides 'perl(String::HexConvert)'
perl -MString::HexConvert=:all -e '
  die "unexpected version\n" unless $String::HexConvert::VERSION eq "0.02";
  die "encode mismatch\n" unless ascii_to_hex("Hello") eq "48656c6c6f";
  die "decode mismatch\n" unless hex_to_ascii("48656c6c6f") eq "Hello";
  my $bytes = "\0\xff\x7f";
  die "binary round-trip mismatch\n"
    unless hex_to_ascii(ascii_to_hex($bytes)) eq $bytes;
'
