#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- dte
test "$(dte -V | head -n 1)" = "dte 1.11.1"
dte -h | grep -F 'Usage:'
dte -B | grep -x rc
work_dir=$(mktemp -d)
trap 'rm -f -- "$work_dir/rc" "$work_dir/dte"; rmdir -- "$work_dir"' EXIT
dte -b rc > "$work_dir/rc"
test -s "$work_dir/rc"
# The syntax loader selects the default syntax by the file's basename.
# Preserve the built-in syntax name, as upstream test/check-opts.sh does.
dte -b syntax/dte > "$work_dir/dte"
dte -s "$work_dir/dte" | grep -E "^OK: loaded syntax 'dte' with [1-9][0-9]* states?$"
test -r /usr/share/man/man1/dte.1.gz || test -r /usr/share/man/man1/dte.1
test -r /usr/share/bash-completion/completions/dte
test -r /usr/share/applications/dte.desktop
test -r /usr/share/metainfo/dte.appdata.xml
