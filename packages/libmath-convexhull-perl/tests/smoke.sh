#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Math-ConvexHull
rpm -q --whatprovides 'perl(Math::ConvexHull)'
perl -MMath::ConvexHull=convex_hull -e '
  die "unexpected version\n" unless $Math::ConvexHull::VERSION eq "1.04";
  my $hull = convex_hull([[0,0], [1,0], [0.2,0.9], [0.2,0.5], [0,1], [1,1]]);
  my $corners = join(q{;}, sort map { join(q{,}, @$_) } @$hull);
  die "unexpected convex hull\n" unless $corners eq "0,0;0,1;1,0;1,1";
'
