#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Regexp-Stringify
perl -MRegexp::Stringify=stringify_regexp -e 'die "stringify" unless stringify_regexp(regexp=>qr/a/,plver=>"5.14.0") eq "(^:a)"'
