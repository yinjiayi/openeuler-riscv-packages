#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-html-quoted
perl -MHTML::Quoted -e '
    die "unexpected version" unless $HTML::Quoted::VERSION eq "0.05";
    my $text = q{Hi,<div><br><div>On date X wrote:<br><blockquote>Hello,<div>How are you?</div></blockquote><div>I&#39;m fine.</div></div></div>};
    my $hunks = HTML::Quoted->extract($text);
    die "nested quote lost" unless grep { ref($_) eq "ARRAY" && $_->[0]{quote} } @$hunks;
    die "HTML round trip failed" unless HTML::Quoted->combine_hunks($hunks) eq $text;
    print "installed HTML::Quoted nesting and round trip passed\n";
'
