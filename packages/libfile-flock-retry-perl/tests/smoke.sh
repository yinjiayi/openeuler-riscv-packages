#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-file-flock-retry
smoke_dir="$(mktemp -d)"
trap 'rmdir -- "$smoke_dir"' EXIT
perl -MFile::Flock::Retry -e '
    my ($path) = @ARGV;
    my $lock = File::Flock::Retry->lock($path, { retries => 0 });
    die "missing lock file" unless -f $path;
    $lock->release or die "release failed";
    die "lock file remains" if -e $path;
    print "ok 1 - installed flock creates and removes lock file\n";
' "$smoke_dir/flock"
