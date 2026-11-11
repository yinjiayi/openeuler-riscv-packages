#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-IO-SessionData
rpm -q --whatprovides 'perl(IO::SessionData)'
rpm -q --whatprovides 'perl(IO::SessionSet)'
perl -MIO::SessionData -MIO::SessionSet -e 'die "wrong class\n" unless IO::SessionSet->SessionDataClass eq "IO::SessionData"'
