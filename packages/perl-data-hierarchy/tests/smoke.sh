#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Data-Hierarchy
perl -MData::Hierarchy -e 'my $t = Data::Hierarchy->new; $t->store("/", {key => "value"}); die "inheritance" unless $t->get("/child")->{key} eq "value"'
