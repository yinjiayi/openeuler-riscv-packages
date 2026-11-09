#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-net-ipv6addr

perl -MNet::IPv6Addr=to_string_compressed,to_bigint,from_bigint -e '
    my $address = "2001:0db8:0000:0000:0000:0000:0000:0001";
    my $compressed = to_string_compressed($address);
    my $roundtrip = from_bigint(to_bigint($address));
    die "unexpected IPv6 compression or integer round-trip\n"
        unless $compressed eq "2001:db8::1"
            && to_string_compressed($roundtrip) eq $compressed;
    print "ok 1 - installed IPv6Addr compresses and round-trips an IPv6 address\n";
'
