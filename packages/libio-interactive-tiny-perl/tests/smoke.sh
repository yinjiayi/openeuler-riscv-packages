#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-io-interactive-tiny
perl -MIO::Interactive::Tiny -e '
    die "unexpected IO::Interactive::Tiny version\n" unless $IO::Interactive::Tiny::VERSION eq "0.2";
    die "redirected input unexpectedly interactive\n" if IO::Interactive::Tiny::is_interactive();
    print "ok - installed module detects non-interactive input\n";
' </dev/null
