#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

test "$(rpm -q --qf '%{VERSION}' perl-Regexp-IPv6)" = '0.03'
perl -MRegexp::IPv6='$IPv6_re' -e '
    die "unexpected module version\n" unless $Regexp::IPv6::VERSION eq "0.03";
    for my $address ("::1", "2001:db8::1", "::ffff:192.0.2.128") {
        die "expected match: $address\n" unless $address =~ /\A(?:$IPv6_re)\z/;
    }
    for my $address ("::", "1::2::3", "2001:db8::zzzz", "127.0.0.1") {
        die "unexpected match: $address\n" if $address =~ /\A(?:$IPv6_re)\z/;
    }
    print "Regexp::IPv6 installed smoke passed\n";
'
