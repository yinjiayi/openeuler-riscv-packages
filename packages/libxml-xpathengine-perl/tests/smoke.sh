#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libxml-xpathengine-perl
/usr/bin/perl - <<'PERL'
use strict;
use warnings;
use XML::XPathEngine;

{
    package LocalNode;
    sub getName       { return $_[0]->{name}; }
    sub get_pos       { return $_[0]->{pos}; }
    sub cmp           { return $_[0]->{pos} <=> $_[1]->{pos}; }
    sub isElementNode { return 1; }
    sub getChildNodes { return wantarray ? @{$_[0]->{children}} : $_[0]->{children}; }
    sub string_value  { return $_[0]->{value}; }
}

my $a = bless { name => 'item', value => 'alpha', pos => 1, children => [] }, 'LocalNode';
my $b = bless { name => 'item', value => 'beta',  pos => 2, children => [] }, 'LocalNode';
my $root = bless { name => 'root', pos => 0, children => [$a, $b] }, 'LocalNode';
my $xpath = XML::XPathEngine->new;
my @result = $xpath->findvalues('child::item', $root);
die "unexpected XPath child results\n" unless join(',', @result) eq 'alpha,beta';
die "unexpected XPath predicate result\n" unless $xpath->findvalue('child::item[2]', $root) eq 'beta';
print "installed XPath child axis and predicate passed\n";
PERL
