#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-IO-Callback
perl -MIO::Callback -e 'my $buf = ""; my $fh = IO::Callback->new(">", sub { $buf .= shift }); print {$fh} "hello"; close $fh; die "callback failed" unless $buf eq "hello";'
