#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-exporter-lite
perl -e '
    {
        package ExporterLiteSmoke;
        use Exporter::Lite;
        our @EXPORT = qw(answer);
        sub answer { 42 }
    }
    ExporterLiteSmoke->import;
    die "unexpected module version\n" unless $Exporter::Lite::VERSION eq "0.09";
    die "default export failed\n" unless answer() == 42;
    print "ok - installed default function export\n";
'
