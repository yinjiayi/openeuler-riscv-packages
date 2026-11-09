#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-lingua-en-inflect-number
perl -MLingua::EN::Inflect::Number=number,to_S,to_PL,PL_N -e '
    die "version\n" unless $Lingua::EN::Inflect::Number::VERSION eq "1.12";
    die "singular\n" unless number("goat") eq "s";
    die "plural\n" unless number("goats") eq "p";
    die "ambiguous\n" unless number("sheep") eq "ambig";
    die "to singular\n" unless to_S("breweries") eq "brewery";
    die "to plural\n" unless to_PL("brewery") eq "breweries";
    die "idempotent\n" unless to_PL("goats") eq "goats" && to_S("goat") eq "goat";
    die "ambiguous conversion\n" unless to_S("sheep") eq "sheep" && to_PL("sheep") eq "sheep";
    die "upstream export\n" unless PL_N("goat") eq "goats";
    print "Lingua::EN::Inflect::Number 1.12 noun conversions passed\n";
'
