#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-file-pathlist
perl -MFile::PathList -MFile::Basename=dirname -e '
use strict; use warnings;
die "version" unless $File::PathList::VERSION eq "1.04";
my $module = $INC{"File/PathList.pm"};
my $paths = File::PathList->new(paths => [dirname($module)], cache => 1);
die "constructor" unless ref($paths) eq "File::PathList";
die "find module" unless $paths->find_file("PathList.pm") eq $module;
die "cached" unless $paths->find_file("PathList.pm") eq $module;
die "missing" unless $paths->find_file("__openeuler_missing_pathlist_file__") eq "";
die "updir" if defined $paths->find_file("../PathList.pm");
die "absolute" if defined $paths->find_file($module);
print "FilePathList installed API smoke passed\n";
'
