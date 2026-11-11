#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-text-csv-separator
fixture=$(mktemp)
trap 'rm -f -- "$fixture"' EXIT
printf '%s\n' '"value: one",alpha' '"value:: two",beta' 'gamma,delta' > "$fixture"
perl -MText::CSV::Separator=get_separator -e '
    die "unexpected Text::CSV::Separator version\n"
        unless $Text::CSV::Separator::VERSION eq "0.20";
    my @separators = get_separator(path => $ARGV[0]);
    die "unexpected CSV delimiter\n" unless @separators == 1 && $separators[0] eq ",";
    print "ok - installed separator selects comma over quoted punctuation\n";
' "$fixture"
