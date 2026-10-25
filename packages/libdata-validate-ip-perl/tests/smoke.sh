#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-Validate-IP
rpm -q --whatprovides 'perl(Data::Validate::IP)'
perl -MData::Validate::IP -e '
  die "unexpected Data::Validate::IP version\n"
    unless $Data::Validate::IP::VERSION eq "0.31";
  die "valid IPv4 rejected\n" unless is_ipv4("192.0.2.9") eq "192.0.2.9";
  die "invalid IPv4 accepted\n" if defined is_ipv4("192.0.2.999");
  die "valid IPv6 rejected\n" unless is_ipv6("2001:db8::1") eq "2001:db8::1";
  die "network membership rejected\n"
    unless is_innet_ipv4("192.0.2.9", "192.0.2.0/24") eq "192.0.2.9";
'
DVI_NO_SOCKET=1 perl -MData::Validate::IP -e '
  die "pure-Perl IPv4 path rejected input\n"
    unless is_ipv4("192.0.2.9") eq "192.0.2.9";
  die "pure-Perl IPv6 path rejected input\n"
    unless is_ipv6("2001:db8::1") eq "2001:db8::1";
'
