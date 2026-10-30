#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Data-DumpXML
perl -MData::DumpXML=dump_xml2 -MData::DumpXML::Parser -e 'my $xml = dump_xml2({key => 33}); my $out = Data::DumpXML::Parser->new->parse($xml); die "roundtrip" unless $out->[0]{key} == 33'
