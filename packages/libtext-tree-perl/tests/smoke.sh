#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-text-tree

perl -MText::Tree -e '
    my $tree = Text::Tree->new("alpha", ["bravo"], ["charlie", ["delta"]]);
    my @layout = $tree->layout("boxed");
    die "unexpected boxed hierarchy\n"
        unless @layout == 11 && $layout[1] =~ /\|alpha\|/
            && $layout[5] =~ /\|bravo\|\s+\|charlie\|/
            && $layout[9] =~ /\|delta\|/;
    print "ok 1 - installed Text::Tree renders boxed siblings and grandchild\n";
'
