#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-tree-dag_node
perl <<'PERL'
use strict;
use warnings;
use Tree::DAG_Node;
die "version" unless $Tree::DAG_Node::VERSION eq '1.39';
my $root=Tree::DAG_Node->new; $root->name('root');
my $child=$root->new_daughter; $child->name('leaf');
die "mother" unless $child->mother == $root;
my @children=$root->daughters;
die "daughters" unless @children==1 && $children[0]==$child;
my $render=join '',@{$root->tree2string({no_attributes=>1})};
die "renderer" unless $render=~/root/ && $render=~/leaf/;
$child->unlink_from_mother;
die "unlink" if $child->mother || scalar($root->daughters);
print "Tree::DAG_Node smoke passed\n";
PERL
