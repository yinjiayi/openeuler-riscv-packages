#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-JSON-MultiValueOrdered
perl -MJSON::MultiValueOrdered -e 'my $j = JSON::MultiValueOrdered->new; my $d = $j->decode(q({"a":1,"a":2})); die "duplicate keys lost" unless join(",", tied(%$d)->get("a")) eq "1,2";'
