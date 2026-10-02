#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Net-IP-Minimal
rpm -q --whatprovides 'perl(Net::IP::Minimal)'
perl -MNet::IP::Minimal=:PROC -e '
  die "unexpected Net::IP::Minimal version\n" unless $Net::IP::Minimal::VERSION eq "0.06";
  die "valid IPv4 rejected\n" unless ip_is_ipv4("172.16.0.216");
  die "invalid IPv4 accepted\n" if ip_is_ipv4("999.1.1.1");
  die "IPv4 version mismatch\n" unless ip_get_version("172.16.0.216") == 4;
  die "valid IPv6 rejected\n" unless ip_is_ipv6("dead:beef:89ab:cdef:0123:4567:89ab:cdef");
  die "invalid IPv6 accepted\n" if ip_is_ipv6("not-an-ip");
  die "IPv6 version mismatch\n" unless ip_get_version("dead:beef:89ab:cdef:0123:4567:89ab:cdef") == 6;
  die "invalid version accepted\n" if defined ip_get_version("not-an-ip");
'
