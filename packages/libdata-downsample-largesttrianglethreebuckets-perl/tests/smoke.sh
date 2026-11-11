#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Data-DownSample-LargestTriangleThreeBuckets
rpm -q --whatprovides 'perl(Data::DownSample::LargestTriangleThreeBuckets)'
perl -MData::DownSample::LargestTriangleThreeBuckets -e 'my $o = Data::DownSample::LargestTriangleThreeBuckets->new(threshold => 3); my $r = $o->lttb([[0,0],[1,1],[2,4],[3,9]]); die "wrong sample count\n" unless @$r == 3'
