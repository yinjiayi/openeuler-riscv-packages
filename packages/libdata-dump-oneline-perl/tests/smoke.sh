#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Data-Dump-OneLine
perl -MData::Dump::OneLine=dmp -e 'die "dump" unless dmp([1,2]) eq "[1,2]"'
