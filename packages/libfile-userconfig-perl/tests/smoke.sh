#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-File-UserConfig
perl -MFile::UserConfig -MFile::ShareDir -e 'my $d = File::ShareDir::dist_dir("File-UserConfig"); die "missing defaults" unless -f "$d/afile.conf";'
