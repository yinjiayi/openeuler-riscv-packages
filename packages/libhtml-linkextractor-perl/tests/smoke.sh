#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libhtml-linkextractor-perl
perl -MHTML::LinkExtractor -e '
    die "unexpected installed version" unless HTML::LinkExtractor->VERSION eq "0.13";
    my $extractor = HTML::LinkExtractor->new(undef, undef, 1);
    $extractor->parse(\q{<a href="https://example.invalid/x">visible</a>});
    my $links = $extractor->links;
    die "unexpected link count" unless @$links == 1;
    die "unexpected link target" unless $links->[0]{href} eq "https://example.invalid/x";
    die "unexpected visible text" unless $links->[0]{_TEXT} eq "visible";
'
