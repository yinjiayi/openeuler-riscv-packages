#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
if [[ "${1:-}" != --staged ]]; then
    rpm -q -- perl-module-extract-version
fi
fixture=$(mktemp)
trap 'rm -f -- "$fixture"' EXIT
printf '%s\n' 'package Fixture;' 'our $VERSION = "1.23";' '1;' > "$fixture"
perl -MModule::Extract::VERSION -e '
    my $v = Module::Extract::VERSION->parse_version_safely($ARGV[0]);
    die "unexpected extracted version\n" unless defined $v && $v eq "1.23";
    print "ok 1 - installed Module::Extract::VERSION extracts a source version\n";
' "$fixture"
