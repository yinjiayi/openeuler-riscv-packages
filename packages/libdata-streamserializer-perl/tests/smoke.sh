#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-StreamSerializer
rpm -q --whatprovides 'perl(Data::StreamSerializer)'
perl -MB -MData::StreamSerializer -e '
  die "wrong installed version\n" unless $Data::StreamSerializer::VERSION eq "0.07";
  die "installed XS entry point inactive\n"
    unless B::svref_2object(\&Data::StreamSerializer::_next)->XSUB;
  my $stream = Data::StreamSerializer->new({answer => [42, "ok"]});
  my $serialized = "";
  while (defined(my $part = $stream->next)) { $serialized .= $part }
  die "installed serializer failed\n"
    unless $serialized =~ /answer/ && $serialized =~ /42/ && $serialized =~ /ok/;
'
