#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-tree-binary
perl <<'PERL'
use strict;
use warnings;
use Tree::Binary;
use Tree::Binary::Visitor::InOrderTraversal;
die "version" unless $Tree::Binary::VERSION eq '1.09';
my $tree=Tree::Binary->new(2)->setLeft(Tree::Binary->new(0))->setRight(Tree::Binary->new(4));
my $visitor=Tree::Binary::Visitor::InOrderTraversal->new;
$tree->accept($visitor);
my @values=$visitor->getResults;
die "in-order values" unless join(',',@values) eq '0,2,4';
die "parent depth" unless $tree->getLeft->getDepth==1;
my $left=$tree->removeLeft;
die "detach" unless $left->getNodeValue==0 && $left->getDepth==0 && !$tree->hasLeft;
print "Tree::Binary smoke passed\n";
PERL
