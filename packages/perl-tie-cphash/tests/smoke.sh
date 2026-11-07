#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-tie-cphash
perl -MTie::CPHash -e '
    die "version" unless $Tie::CPHash::VERSION eq "2.000";
    tie my %h, "Tie::CPHash";
    $h{Alpha}=1;
    die "lookup" unless $h{alpha} == 1 && exists $h{ALPHA};
    die "spelling" unless tied(%h)->key("ALPHA") eq "Alpha";
    $h{ALPHA}=2;
    die "replace" unless $h{alpha} == 2 && tied(%h)->key("alpha") eq "ALPHA";
    die "duplicate" unless scalar(keys %h) == 1;
    die "delete" unless delete($h{aLpHa}) == 2 && !exists $h{ALPHA};
'
