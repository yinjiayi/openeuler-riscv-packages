#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Data-Dmp
perl -MData::Dmp=dmp -e 'die "dump" unless dmp([1,2,3]) eq "[1,2,3]"'
