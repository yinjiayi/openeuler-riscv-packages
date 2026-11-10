#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-package-new
perl -MPackage::New::Dump <<'PERL'
use strict;
use warnings;
my $object = Package::New::Dump->new(answer => 42);
die "bad constructor" unless ref($object) eq 'Package::New::Dump'
    && $object->isa('Package::New') && $object->{answer} == 42;
my $dump = $object->dump;
if (eval { require Data::Dumper; 1 }) {
    die "bad serialization" unless $dump =~ /answer.*42/;
} else {
    die "bad optional fallback" unless $dump eq '';
}
print "ok 1 - installed Package::New constructor and optional serialization\n";
PERL
