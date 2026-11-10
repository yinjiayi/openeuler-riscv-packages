#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-class-std-utils
perl -MClass::Std::Utils -e '
    my $ref = anon_scalar();
    die "anonymous scalar mismatch\n" unless ref($ref) eq "SCALAR" && !defined $$ref;
    my $other = anon_scalar();
    my $id = ident($ref);
    die "unstable or reused identity\n" unless defined $id && $id == ident($ref) && $id != ident($other);
    print "installed anonymous scalar and stable identity passed\n";
'
