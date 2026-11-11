#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Data-Hexify
rpm -q --whatprovides 'perl(Data::Hexify)'
perl -MData::Hexify -e 'my $dump = Hexify("A"); die "missing byte\n" unless $dump =~ /41/'
