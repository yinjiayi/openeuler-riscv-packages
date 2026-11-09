#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libnet-cidr-perl
unset PERL5LIB PERLLIB PERL5OPT
/usr/bin/perl - <<'PERL'
use strict;
use warnings;
use Net::CIDR;

die "IPv4 inclusion failed" unless Net::CIDR::cidrlookup('192.0.2.7', '192.0.2.0/24');
die "IPv4 exclusion failed" if Net::CIDR::cidrlookup('192.0.3.7', '192.0.2.0/24');
die "IPv6 inclusion failed" unless Net::CIDR::cidrlookup('2001:db8::7', '2001:db8::/32');
print "installed IPv4 and IPv6 CIDR lookup passed\n";
PERL
