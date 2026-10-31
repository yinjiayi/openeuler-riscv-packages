#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-File-NCopy
rpm -q --whatprovides 'perl(File::NCopy)'
perl -MFile::NCopy -e 'die "missing object\n" unless File::NCopy->new(test => 1)'
