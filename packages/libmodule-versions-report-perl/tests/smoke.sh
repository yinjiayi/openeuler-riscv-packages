#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
perl -MFcntl -e '
    use Module::Versions::Report ();
    my $report = Module::Versions::Report::report();
    die "missing loaded module version" unless $report =~ /Modules in memory:/
        && $report =~ /Module::Versions::Report v1\.06/
        && $report =~ /Fcntl v\Q$Fcntl::VERSION\E/;
    print "ok - reports the installed module and loaded Fcntl version\n";
'
