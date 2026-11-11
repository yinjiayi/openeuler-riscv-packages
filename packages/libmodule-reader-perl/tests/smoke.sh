#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-module-reader
perl -MModule::Reader=module_content,module_handle -e '
    die "unexpected module version\n" unless $Module::Reader::VERSION == 0.003003;
    my $source = module_content("Module::Reader");
    my $handle = module_handle("Module::Reader");
    local $/;
    die "module source did not round trip\n"
        unless $source =~ /^package Module::Reader;/m && <$handle> eq $source;
    print "installed module source and handle agree\n";
'
