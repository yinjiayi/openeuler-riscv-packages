#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-File-Save-Home
perl -MFile::Save::Home -e 'die "module" unless File::Save::Home->can("get_home_directory")'
