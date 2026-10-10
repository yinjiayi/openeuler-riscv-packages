#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-Buffer
rpm -q --whatprovides 'perl(Data::Buffer)'
perl -e '
  use Data::Buffer;
  die "unexpected Data::Buffer version\n"
    unless $Data::Buffer::VERSION eq "0.06";
  my $buffer = Data::Buffer->new;
  $buffer->put_int16(1234);
  die "binary buffer round-trip mismatch\n" unless $buffer->get_int16 == 1234;
'
