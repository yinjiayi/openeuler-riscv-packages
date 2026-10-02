#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Net-MAC
rpm -q --whatprovides 'perl(Net::MAC)'
perl -MNet::MAC -e '
  die "unexpected Net::MAC version\n" unless $Net::MAC::VERSION eq "2.103622";
  my $mac = Net::MAC->new(mac => "08:20:00:AB:CD:EF");
  die "Cisco format mismatch\n" unless $mac->as_Cisco eq "0820.00ab.cdef";
  my $decimal = $mac->convert(base => 10, bit_group => 8, delimiter => ".");
  die "decimal conversion mismatch\n" unless $decimal->get_mac eq "8.32.0.171.205.239";
  my $invalid = Net::MAC->new(mac => "invalid", die => 0);
  die "invalid address was accepted\n" unless $invalid->get_error;
'
