#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-File-Pid
rpm -q --whatprovides 'perl(File::Pid)'
perl -MFile::Pid -e 'die "wrong current pid\n" unless File::Pid->new({file => "/dev/null", pid => $$})->pid == $$'
