#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-file-dircompare
stage=$(mktemp -d)
trap 'rm -r -- "$stage"' EXIT
mkdir "$stage/left" "$stage/right"
printf 'left\n' > "$stage/left/changed"
printf 'right\n' > "$stage/right/changed"
printf 'same\n' > "$stage/left/same"
printf 'same\n' > "$stage/right/same"
printf 'unique\n' > "$stage/right/unique"
perl -MFile::DirCompare -MFile::Basename -e '
    die "wrong version\n" unless $File::DirCompare::VERSION eq "0.7";
    my @got;
    File::DirCompare->compare(@ARGV, sub {
        my ($a, $b) = @_;
        push @got, join ":", map { defined $_ ? basename($_) : "-" } ($a, $b);
    });
    die "wrong differences: @got\n" unless "@got" eq "changed:changed -:unique";
' "$stage/left" "$stage/right"
