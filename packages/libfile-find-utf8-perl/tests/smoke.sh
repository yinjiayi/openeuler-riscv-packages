#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-file-find-utf8
perl -MFile::Find::utf8 -MFile::Temp=tempdir -MEncode=encode_utf8 -Mutf8 -e '
    my $d = tempdir(CLEANUP => 1);
    my $name = "文件.txt";
    open my $f, ">", encode_utf8("$d/$name") or die $!;
    close $f or die $!;
    my @found;
    find(sub { push @found, $_ }, $d);
    die "UTF-8 path absent" unless grep { $_ eq $name } @found;
    print "installed UTF-8 path discovery passed\n";
'
