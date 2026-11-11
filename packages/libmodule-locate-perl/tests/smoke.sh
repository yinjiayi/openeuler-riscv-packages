#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-module-locate
perl -T -MModule::Locate=locate,mod_to_path -e '
    die "installed Module::Locate not found" unless locate("Module::Locate") eq $INC{"Module/Locate.pm"};
    die "core module not found" unless locate("strict") =~ m{(?:^|/)strict[.]pm\z};
    die "wrong module path" unless mod_to_path("Foo::Bar") eq "Foo/Bar.pm";
    print "installed Module::Locate finds modules without loading them\n";
'
