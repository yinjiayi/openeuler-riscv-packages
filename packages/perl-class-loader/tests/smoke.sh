#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Class-Loader
perl -e 'package Local::Probe; use Class::Loader; our @ISA=("Class::Loader"); sub new { bless {}, shift } package main; my $p=Local::Probe->new; my $o=$p->_load(Module=>"Class::LoaderTest"); die "loader" unless ref($o) eq "Class::LoaderTest" && $o->{Method} eq "new"'
