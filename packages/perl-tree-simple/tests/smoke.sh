#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
set -eu
perl -MTree::Simple -MTree::Simple::Visitor -e '
  my $root = Tree::Simple->new("root");
  my $child = Tree::Simple->new("child");
  $root->addChild($child);
  die "bad child link" unless $root->getChildCount == 1 && $child->getParent == $root;
  print "ok - parent and child links\n";
  my $clone = $root->clone;
  die "bad clone" unless $clone != $root && $clone->getChild(0)->getNodeValue eq "child";
  print "ok - clones child data\n";
  my $visitor = Tree::Simple::Visitor->new;
  $visitor->visit($root);
  my @seen = $visitor->getResults;
  die "bad visit" unless @seen == 1 && $seen[0] eq "child";
  print "ok - visitor traverses child\n";
'
