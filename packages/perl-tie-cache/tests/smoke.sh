#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Tie-Cache
perl <<'PERL'
use strict;
use warnings;
use Tie::Cache;
die "version" unless $Tie::Cache::VERSION eq '0.21';
tie my %cache, 'Tie::Cache', 2;
$cache{a} = 1;
$cache{b} = 2;
die "read" unless $cache{a} == 1;
$cache{c} = 3;
die "least recently used eviction" if exists $cache{b};
die "retained entries" unless $cache{a} == 1 && $cache{c} == 3;
die "delete" unless delete($cache{a}) == 1 && !exists($cache{a});
$cache{object} = { answer => 42 };
die "reference value" unless $cache{object}{answer} == 42;
%cache = ();
die "clear" if keys %cache;
print "Tie::Cache installed API checks passed\n";
PERL
