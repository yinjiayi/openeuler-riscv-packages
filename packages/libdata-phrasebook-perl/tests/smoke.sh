#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Data-Phrasebook
perl -MData::Phrasebook -e 'my $p = Data::Phrasebook->new; die "unexpected class" unless $p->isa("Data::Phrasebook::Plain");'
