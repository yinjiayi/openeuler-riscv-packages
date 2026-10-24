#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-StreamDeserializer
rpm -q --whatprovides 'perl(Data::StreamDeserializer)'
perl -MData::StreamDeserializer -e '
  die "unexpected version\n" unless $Data::StreamDeserializer::VERSION eq "0.06";
  my $reader = Data::StreamDeserializer->new(data => q# { "a" => [ 1, 2 ] } #);
  1 until $reader->next;
  die $reader->error if $reader->is_error;
  my $result = $reader->result;
  die "unexpected parsed value\n" unless ref($result) eq "HASH"
    && ref($result->{a}) eq "ARRAY" && $result->{a}[1] == 2;
'
