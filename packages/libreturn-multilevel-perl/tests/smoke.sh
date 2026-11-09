#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-return-multilevel

perl -MReturn::MultiLevel=with_return -e '
    sub bounce {
        my ($return) = @_;
        $return->("one", "two");
        die "return callback did not escape";
    }
    my @values = with_return { bounce($_[0]); die "unreachable" };
    die "wrong nested return values" unless "@values" eq "one two";
    my $backend = $Return::MultiLevel::_backend;
    die "unrecognized backend" unless $backend eq "PP" || $backend eq "XS";
    my $label = $backend eq "PP" ? "pure Perl" : "XS";
    print "ok 1 - installed Return::MultiLevel escapes nested call using default $label backend\n";
'
