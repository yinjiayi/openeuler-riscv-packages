#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libsort-key-top-perl
perl -MSort::Key::Top=topsort -e '
    die "incorrect native top-k ordering\n"
        unless join(",", topsort(2, qw(fox ant bee))) eq "ant,bee";
    die "native Sort::Key::Top XS module did not load\n"
        unless grep { m{/auto/Sort/Key/Top/Top[.]so$} } @DynaLoader::dl_shared_objects;
    print "installed native top-k sorts correctly\n";
'
