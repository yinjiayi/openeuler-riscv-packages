#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libscalar-util-numeric-perl
perl -MScalar::Util::Numeric=isint,isfloat,isnum -e '
    die "version" unless Scalar::Util::Numeric->VERSION eq "0.40";
    die "numeric predicates"
        unless isint("-42") == -1 && isfloat("3.25") && !isnum("not numeric");
    print "installed native XS predicates passed\n";
'
