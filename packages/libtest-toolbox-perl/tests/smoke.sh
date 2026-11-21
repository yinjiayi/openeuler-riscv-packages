#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
perl -MTest::Toolbox -e '
    rtplan 2;
    rtarr("installed Toolbox compares unordered values", [qw(a b)], [qw(b a)], order_insensitive => 1);
    rteval("installed Toolbox checks captured error", sub { die "fixture-error: from test" }, "fixture-error");
'
