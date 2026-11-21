#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-file-tee
work=$(mktemp -d)
trap 'rmdir "$work" 2>/dev/null || true' EXIT
perl -MFile::Tee=tee - "$work" <<'PERL'
use strict;
use warnings;
my ($dir) = @ARGV;
open my $out, '>', "$dir/original" or die $!;
my $pid = tee($out, {open => ['>', "$dir/copy"]}) or die 'tee failed';
my $bytes = "first\nsecond\n";
print {$out} $bytes or die $!;
close $out or die $!;
waitpid($pid, 0);
for my $file (qw(original copy)) {
    open my $in, '<', "$dir/$file" or die $!;
    my $contents = do { local $/; <$in> };
    die "tee content mismatch: $file" unless $contents eq $bytes;
    close $in or die $!;
    unlink "$dir/$file" or die $!;
}
print "installed File::Tee duplicated exact bytes\n";
PERL
