#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libdns-zoneparse-perl
unset PERL5LIB PERLLIB PERL5OPT
/usr/bin/perl - <<'PERL'
use strict;
use warnings;
use DNS::ZoneParse;

my $input = <<'ZONE';
$TTL 3600
@ IN SOA ns.example.test. admin.example.test. (1 7200 900 1209600 300)
www IN A 192.0.2.23
ZONE
sub check_zone {
    my ($text) = @_;
    my $zone = DNS::ZoneParse->new(\$text, 'example.test.');
    die "unexpected zone data" unless !$zone->last_parse_error_count
        && $zone->soa->{serial} == 1 && @{$zone->a} == 1
        && $zone->a->[0]{host} eq '192.0.2.23'
        && $zone->fqname($zone->a->[0]) eq 'www.example.test.';
    return $zone;
}
my $parsed = check_zone($input);
check_zone($parsed->output);
print "installed DNS A/SOA roundtrip passed\n";
PERL
