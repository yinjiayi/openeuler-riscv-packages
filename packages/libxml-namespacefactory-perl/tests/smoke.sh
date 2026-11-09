#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libxml-namespacefactory-perl
/usr/bin/perl - <<'PERL'
use strict;
use warnings;
use XML::NamespaceFactory;

my $ns = XML::NamespaceFactory->new('urn:codex:test:');
die "unexpected method-based Clark name\n"
    unless $ns->title eq '{urn:codex:test:}title';
die "unexpected tied-hash Clark name\n"
    unless $ns->{'x.y-z'} eq '{urn:codex:test:}x.y-z';
print "installed SAX Clark names passed\n";
PERL
