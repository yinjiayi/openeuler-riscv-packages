#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-IO-CaptureOutput
rpm -q --whatprovides 'perl(IO::CaptureOutput)'
perl -MIO::CaptureOutput=capture -e 'my ($out,$err); capture(sub { print "ok"; print STDERR "err" }, \$out, \$err); die "capture failed\n" unless $out eq "ok" && $err eq "err"'
