#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-aliased
perl -Mstrict -Mwarnings -e '
    use aliased "File::Spec" => "PathSpec";
    die "alias mismatch" unless PathSpec eq "File::Spec";
    die "class dispatch failed" unless PathSpec->catfile("a", "b") eq "a/b";
    use aliased;
    my $prefix = prefix("File");
    die "prefix mismatch" unless $prefix->("Spec") eq "File::Spec";
'
