#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libstatistics-distributions-perl
autosplit=$(rpm -ql -- libstatistics-distributions-perl | grep -E '/auto/Statistics/Distributions/autosplit[.]ix$')
[[ -s $autosplit ]]
perl -MStatistics::Distributions -e '
    die "unexpected installed version" unless Statistics::Distributions->VERSION eq "1.02";
    die "unexpected chi-square quantile" unless abs(Statistics::Distributions::chisqrdistr(2, 0.05) - 5.9915) < 1e-10;
    die "unexpected normal quantile" unless abs(Statistics::Distributions::udistr(0.05) - 1.6449) < 1e-10;
'
