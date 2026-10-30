#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Class-Member
perl -e 'package Local::Probe; use Class::Member::HASH qw/value/; sub new { bless {}, shift } package main; my $p = Local::Probe->new; $p->value("ok"); die "accessor" unless $p->value eq "ok"'
