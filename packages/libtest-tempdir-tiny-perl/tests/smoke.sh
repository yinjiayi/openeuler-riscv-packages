#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
perl -MTest::TempDir::Tiny  -MCwd=abs_path -e '
    print qq(1..4\n);
    my $n = 0;
    my $assert = sub {
        my ($passed, $name) = @_;
        ++$n;
        die qq(not ok $n - $name\n) unless $passed;
        print qq(ok $n - $name\n);
    };
    my $cwd = abs_path(".");
    my $seen;
    in_tempdir "packaged-smoke" => sub {
        my ($dir) = @_;
        $seen = $dir;
        $assert->(abs_path(".") eq abs_path($dir), "installed temp helper enters actual directory");
        open my $fixture, ">", "sentinel" or die $!;
        print {$fixture} "exact-target\n";
        close $fixture or die $!;
    };
    $assert->(abs_path(".") eq $cwd, "installed temp helper restores caller directory");
    $assert->(-f "$seen/sentinel", "installed temp helper uses the returned directory");
    $assert->(tempdir("distinct") ne $seen, "installed named temporary directory stays distinct");
'
