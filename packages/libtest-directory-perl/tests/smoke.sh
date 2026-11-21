#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
scratch=$(mktemp -d "${TMPDIR:-/tmp}/test-directory-smoke.XXXXXXXX")
trap 'rmdir -- "$scratch"' EXIT
perl -MTest::Directory -e '
    my $path = shift;
    my $directory = Test::Directory->new($path);
    $directory->create("entry", content => "abc");
    die "fixture was not created" unless $directory->check_file("entry")
        && -s $directory->path("entry") == 3;
    undef $directory;
    die "fixture was not cleaned" if -e $path;
    print "ok - installed Test::Directory creates, finds and cleans a file\n";
' "$scratch/managed"
