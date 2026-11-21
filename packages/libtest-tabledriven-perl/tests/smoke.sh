#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-test-tabledriven
perl -MTest::TableDriven -e '
Test::TableDriven->import(double => [[2, 4], [3, 6]]);
sub double { return 2 * $_[0] }
runtests();
'
