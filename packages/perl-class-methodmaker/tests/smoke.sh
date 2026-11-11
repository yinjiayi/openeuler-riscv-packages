#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Class-MethodMaker
perl -e 'package Local::Probe; use Class::MethodMaker [scalar => [qw/value/]]; package main; my $o=bless {}, "Local::Probe"; $o->value("ok"); die "accessor" unless $o->value eq "ok"'
