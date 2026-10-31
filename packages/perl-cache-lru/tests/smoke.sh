#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Cache-LRU
perl -MCache::LRU -e '
  die "unexpected version\n" unless $Cache::LRU::VERSION eq "0.04";
  my $cache = Cache::LRU->new(size => 1);
  $cache->set(a => 1); $cache->set(b => 2);
  die "eviction failed\n" if defined $cache->get("a");
  die "lookup failed\n" unless $cache->get("b") == 2;
'
