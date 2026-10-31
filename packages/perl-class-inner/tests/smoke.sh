#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Class-Inner
perl -e 'use Class::Inner; package Local::Parent; sub new { bless {}, shift } sub value { "original" } package main; my $p=Class::Inner->new(parent=>"Local::Parent", methods=>{value=>sub { "changed" }}); die "override" unless $p->isa("Local::Parent") && $p->value eq "changed"'
