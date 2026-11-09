#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libconfig-grammar-perl
config=$(mktemp)
trap 'rm -f -- "$config"' EXIT
printf '%s\n' 'limit = 24' > "$config"
perl -MConfig::Grammar -MConfig::Grammar::Dynamic -MConfig::Grammar::Document -e '
    die "unexpected installed version" unless Config::Grammar->VERSION eq "1.13";
    my $parser = Config::Grammar->new({_vars => ["limit"], limit => {_re => qr/^[0-9]+$/}});
    my $parsed = $parser->parse($ARGV[0]);
    die "configuration did not parse" unless $parsed && $parsed->{limit} eq "24";
' "$config"
