#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-io-capture
perl -MIO::Capture::Stdout -MIO::Capture::Stderr <<'PERL'
use strict;
use warnings;
my $out = IO::Capture::Stdout->new;
my $err = IO::Capture::Stderr->new;
$out->start or die "stdout start";
$err->start or die "stderr start";
print STDOUT "capture stdout\n";
print STDERR "capture stderr\n";
$err->stop or die "stderr stop";
$out->stop or die "stdout stop";
die "wrong output" unless $out->read eq "capture stdout\n" && $err->read eq "capture stderr\n";
print "ok 1 - installed IO::Capture captures both streams and restores the original handles\n";
PERL
