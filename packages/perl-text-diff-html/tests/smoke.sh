#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-text-diff-html
perl -MText::Diff -MText::Diff::HTML -e '
    die "unexpected Text::Diff::HTML version\n" unless $Text::Diff::HTML::VERSION eq "0.08";
    my ($old, $new) = ("old <a>\n", "new &\n");
    my $html = diff(\$old, \$new, { STYLE => "Text::Diff::HTML" });
    die "unescaped or missing diff content\n" unless $html =~ /&lt;a&gt;/ && $html =~ /&amp;/;
    print "ok - installed diff escapes local input\n";
'
