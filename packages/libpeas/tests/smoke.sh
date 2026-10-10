#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libpeas libpeas-devel
rpm -q --whatprovides 'pkgconfig(libpeas-1.0)'
rpm -q --whatprovides 'pkgconfig(libpeas-gtk-1.0)'
