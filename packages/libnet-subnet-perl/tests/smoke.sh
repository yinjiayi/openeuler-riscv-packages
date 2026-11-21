#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libnet-subnet-perl
perl -MNet::Subnet -e '
  use strict;
  use warnings;
  my @cidrs = sort_subnets(qw(192.0.2.0/24 2001:db8::/32 2001:db8:20::/48));
  my $in_cidr = subnet_matcher(@cidrs);
  my $classify = subnet_classifier(@cidrs);
  die "IPv4 mask" unless $in_cidr->("192.0.2.17") && !$in_cidr->("192.0.3.17");
  die "IPv6 prefix priority" unless $classify->("2001:db8:20::1") eq "2001:db8:20::/48"
      && $classify->("2001:db8:21::1") eq "2001:db8::/32";
  die "unmatched IPv6 address" if defined $classify->("2001:db9::1");
  print "installed numeric IPv4/IPv6 CIDR and longest-prefix classification passed\n";
'
