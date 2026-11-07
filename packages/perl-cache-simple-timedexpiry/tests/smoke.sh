#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Cache-Simple-TimedExpiry
perl <<'PERL'
use strict;
use warnings;
use Cache::Simple::TimedExpiry;
die "module version mismatch\n" unless $Cache::Simple::TimedExpiry::VERSION eq '0.27';
my $cache = Cache::Simple::TimedExpiry->new;
$cache->expire_after(60);
die "expiry policy mismatch\n" unless $cache->expire_after == 60;
$cache->store('alpha', 'one');
$cache->set(0, 'zero');
$cache->set('', 'empty');
die "fetch mismatch\n" unless $cache->fetch('alpha') eq 'one';
die "get alias mismatch\n" unless $cache->get(0) eq 'zero';
die "empty key mismatch\n" unless $cache->get('') eq 'empty';
die "missing key mismatch\n" if $cache->has_key('absent');
die "key inventory mismatch\n" unless join(',', sort $cache->elements) eq ',0,alpha';
$cache->expire(time + 120);
die "explicit expiration mismatch\n" if $cache->has_key('alpha') || $cache->elements;
print "Cache::Simple::TimedExpiry installed API checks passed\n";
PERL
