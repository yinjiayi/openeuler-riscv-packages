#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libstatistics-linefit-perl
[[ $(rpm -q --qf '%{VERSION}' -- libstatistics-linefit-perl) == '0.07' ]]
perl -MStatistics::LineFit -e '
    die "unexpected upstream module version" unless Statistics::LineFit->VERSION eq "0.06";
    my $fit = Statistics::LineFit->new;
    die "missing release 0.07 feature" unless $fit->can("varianceOfEstimates");
    die "could not fit test data" unless $fit->setData([1, 2, 3], [3, 5, 7]);
    my ($intercept, $slope) = $fit->coefficients;
    die "unexpected coefficients" unless abs($intercept - 1) < 1e-10 && abs($slope - 2) < 1e-10;
'
