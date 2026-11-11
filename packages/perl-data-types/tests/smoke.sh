#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Data-Types
perl -MData::Types=is_int,to_int -e 'die "is_int" unless is_int(-42); die "to_int" unless to_int(3.6) == 4'
