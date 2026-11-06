#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- dte
test "$(dte -V | head -n 1)" = "dte 1.11.1"
dte -h | grep -F 'Usage:'
dte -B | grep -x rc
work_dir=$(mktemp -d)
trap 'rm -f -- "$work_dir/rc" "$work_dir/syntax"; rmdir -- "$work_dir"' EXIT
dte -b rc > "$work_dir/rc"
test -s "$work_dir/rc"
dte -b syntax/dte > "$work_dir/syntax"
dte -s "$work_dir/syntax"
test -r /usr/share/man/man1/dte.1.gz || test -r /usr/share/man/man1/dte.1
test -r /usr/share/bash-completion/completions/dte
test -r /usr/share/applications/dte.desktop
test -r /usr/share/metainfo/dte.appdata.xml
