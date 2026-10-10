#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Net-CIDR-Set
rpm -q --whatprovides 'perl(Net::CIDR::Set)'
perl -MNet::CIDR::Set -e '
  die "unexpected Net::CIDR::Set version\n" unless $Net::CIDR::Set::VERSION eq "0.23";
  my $v4 = Net::CIDR::Set->new("192.0.2.0/24");
  $v4->remove("192.0.2.1");
  my @v4 = $v4->as_range_array;
  die "IPv4 subtraction mismatch\n"
    unless @v4 == 2 && $v4[0] eq "192.0.2.0" && $v4[1] eq "192.0.2.2-192.0.2.255";
  my $v6 = Net::CIDR::Set->new("2001:db8::/32");
  my @v6 = $v6->as_cidr_array(1);
  die "IPv6 CIDR mismatch\n" unless @v6 == 1 && $v6[0] eq "2001:db8::/32";
'
