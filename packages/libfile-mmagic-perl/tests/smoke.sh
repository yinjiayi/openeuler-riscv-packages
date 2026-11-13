#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-file-mmagic
perl -MFile::MMagic -e '
    my $magic = File::MMagic->new;
    die "plain text was not recognized\n"
        unless $magic->checktype_contents("a plain text line\n") eq "text/plain";
    $magic->addMagicEntry("0\tstring\tMMAGIC-TEST\tapplication/x-mmagic-test");
    die "custom magic rule did not match\n"
        unless $magic->checktype_contents("MMAGIC-TEST example") eq "application/x-mmagic-test";
    print "installed File::MMagic plain and custom magic checks passed\n";
'
