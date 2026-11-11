#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libset-crontab-perl
perl -MSet::Crontab -e '
    die "unexpected installed version" unless Set::Crontab->VERSION eq "1.03";
    my $set = Set::Crontab->new("1-9/3,!4", [0..9]);
    die "unexpected list" unless join(",", $set->list) eq "1,7";
    die "unexpected membership" unless $set->contains(7) && !$set->contains(4);
'
