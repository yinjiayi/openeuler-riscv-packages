#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libtest-more-utf8-perl
tap=$(perl -MTest::More -MTest::More::UTF8 -e '
    die "unexpected installed version" unless Test::More::UTF8->VERSION eq "0.05";
    die "UTF-8 source text was not enabled" unless utf8::is_utf8("星");
    is("星", "星", "星");
    done_testing;
')
[[ $tap == $'ok 1 - 星\n1..1' ]]
