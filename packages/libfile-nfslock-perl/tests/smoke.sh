#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-file-nfslock
perl <<'PERL'
use strict;
use warnings;
use File::Temp qw(tempdir);
use File::NFSLock;
my $dir = tempdir(CLEANUP => 1);
my $file = "$dir/data";
open my $out, '>', $file or die $!;
print {$out} "private lock test\n" or die $!;
close $out or die $!;
my $lock = File::NFSLock->new($file, 'NONBLOCKING', 1, 30)
    or die $File::NFSLock::errstr;
die 'lock file missing' unless -f "$file.NFSLock";
die 'unlock failed' unless $lock->unlock;
die 'lock file left behind' if -e "$file.NFSLock";
print "ok - installed File::NFSLock private lock lifecycle\n";
PERL
