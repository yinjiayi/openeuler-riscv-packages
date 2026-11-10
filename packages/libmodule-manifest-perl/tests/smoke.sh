#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libmodule-manifest-perl
perl -MModule::Manifest -e '
    my $parsed = Module::Manifest->new;
    $parsed->parse(manifest => ["lib/Example.pm"]);
    $parsed->parse(skip => ["(^|/)\\.git(/|\$)"]);
    my @files = $parsed->files;
    die "manifest entry mismatch" unless @files == 1 && $files[0] eq "lib/Example.pm";
    die "manifest skip rule mismatch" unless $parsed->skipped("a/.git/config")
        && !$parsed->skipped("lib/Example.pm");
    print "installed manifest parse and skip rules passed\n";
'
