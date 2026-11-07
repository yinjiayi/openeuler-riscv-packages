#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-tree-multinode
perl <<'PERL'
use strict;
use warnings;
use Tree::MultiNode;
die "version" unless $Tree::MultiNode::VERSION eq '2.02';
my $tree=Tree::MultiNode->new;
my $h=Tree::MultiNode::Handle->new($tree);
$h->add_child('first',10);
$h->add_child('zero',0);
my %pairs=$h->kv_pairs;
die "values" unless $pairs{first}==10 && exists($pairs{zero}) && $pairs{zero}==0;
my @removed=$h->remove_child(0);
die "remove" unless $removed[0] eq 'first' && $removed[1]==10;
my @keys=$h->child_keys;
die "remaining" unless @keys==1 && $keys[0] eq 'zero';
my $node=Tree::MultiNode::Node->new(0,'');
die "false key" unless defined($node->key) && $node->key==0;
print "Tree::MultiNode smoke passed\n";
PERL
