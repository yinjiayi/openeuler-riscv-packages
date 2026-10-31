#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Class-Mix
perl -MClass::Mix=mix_class -e 'package Local::A; package Local::B; package main; my $c=mix_class("Local::A", "Local::B"); die "mix" unless $c->isa("Local::A") && $c->isa("Local::B")'
