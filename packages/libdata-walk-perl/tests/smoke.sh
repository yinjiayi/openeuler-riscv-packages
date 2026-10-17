#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
perl -MData::Walk -e '
die "version\n" unless $Data::Walk::VERSION eq "2.01";
my $data = [1, [2, 3]]; my @pre; my @post;
Data::Walk::walk(sub { push @pre, ref($_) ? "ARRAY" : $_ }, $data);
Data::Walk::walkdepth(sub { push @post, ref($_) ? "ARRAY" : $_ }, $data);
die "traversal order\n" unless join(",", @pre) eq "ARRAY,1,ARRAY,2,3" && join(",", @post) eq "1,2,3,ARRAY,ARRAY";
my $cycle = {}; $cycle->{self}=$cycle; $cycle->{value}=7; my $count=0;
Data::Walk::walk(sub { ++$count }, $cycle);
die "cycle traversal\n" unless $count==5;
my $blessed = bless [4,5], "Local::WalkSmoke"; my @depth;
Data::Walk::walk(sub { push @depth, $Data::Walk::depth }, $blessed);
die "blessing\n" unless ref($blessed) eq "Local::WalkSmoke";
die "depth\n" unless join(",", @depth) eq "1,2,2";
'
cd /usr/share/licenses/perl-Data-Walk
sha256sum --check <<'HASHES'
5bbcbb737e60fe9deba08ecbd00920cfcc3403ba2e534c64fdeea49d6bb87509  COPYING.LESSER
2facb36fac40a6c53964b1459d909d72a65665b95cb3bb1e531cd1dc74af39a2  perl-5.8.7-README
b7fd9b73ea99602016a326e0b62e6646060d18febdd065ceca8bb482208c3d88  perl-5.8.7-Artistic
9e57f5bc2cfc54e08afc80163c29006f38d9f9c890ebd4efe3c25f0d48b65a52  perl-5.8.7-Copying
4a8884d10b201abf402356f8ff340a0e66816f206b4dd5789ec612bfdfca98bf  PERL-POD-ORIGIN
HASHES
