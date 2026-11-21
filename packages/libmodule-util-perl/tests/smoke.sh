#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-module-util
module_path=$(perl -MModule::Util -e '
    die "unexpected Module::Util version\n" unless $Module::Util::VERSION eq "1.09";
    print $INC{"Module/Util.pm"};
')
test "$(pm_which Module::Util)" = "$module_path"
printf '%s\n' 'ok - installed pm_which locates the same Module::Util module'
