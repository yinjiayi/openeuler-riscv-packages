#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- autoconf-archive
test -f /usr/share/aclocal/ax_check_compile_flag.m4
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
printf '%s\n' 'AC_INIT([smoke],[1])' 'AC_CONFIG_SRCDIR([configure.ac])' 'AX_CHECK_COMPILE_FLAG([-Wall])' 'AC_OUTPUT' >"$d/configure.ac"
(cd "$d" && autoreconf -fi && ./configure)
