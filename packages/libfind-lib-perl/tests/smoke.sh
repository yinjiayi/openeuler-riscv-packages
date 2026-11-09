#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libfind-lib-perl
unset PERL5LIB PERLLIB PERL5OPT
tmp=$(mktemp -d)
trap 'rm -rf -- "$tmp"' EXIT
mkdir -p "$tmp/app" "$tmp/private" "$tmp/elsewhere"
printf '%s\n' 'package FenceFixture;' 'sub marker { 42 }' '1;' > "$tmp/private/FenceFixture.pm"
printf '%s\n' "use Find::Lib '../private';" 'use FenceFixture;' \
    'die "unexpected private fixture" unless FenceFixture::marker() == 42;' \
    'print "installed script-relative fixture passed\n";' > "$tmp/app/check.pl"
cd "$tmp/elsewhere"
/usr/bin/perl "$tmp/app/check.pl"
