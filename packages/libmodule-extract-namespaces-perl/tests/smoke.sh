#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-module-extract-namespaces
fixture=$(mktemp)
trap 'rm -f -- "$fixture"' EXIT
printf '%s\n' 'package Local::Alpha;' 'package Local::Beta;' 'die "input was executed";' > "$fixture"
perl -MModule::Extract::Namespaces -e '
    die "unexpected Module::Extract::Namespaces version\n"
        unless $Module::Extract::Namespaces::VERSION eq "1.026";
    my @packages = Module::Extract::Namespaces->from_file($ARGV[0]);
    die "unexpected namespaces\n" unless join(",", @packages) eq "Local::Alpha,Local::Beta";
    print "ok - installed namespaces extracts two packages in order\n";
' "$fixture"
