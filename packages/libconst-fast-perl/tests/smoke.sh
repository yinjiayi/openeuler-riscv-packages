#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libconst-fast-perl
perl -MConst::Fast -e '
    const my $value => 42;
    die "constant value not preserved\n" unless $value == 42;
    my $changed = eval { $value = 1; 1 };
    die "constant not protected\n" if $changed || $@ !~ /read-only/ || $value != 42;
    print "installed Const::Fast protects a read-only scalar\n";
'
