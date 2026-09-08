#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- gdbm gdbm-libs gdbm-devel

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
database=$smoke_dir/smoke.gdbm
dump_file=$smoke_dir/smoke.dump
restored=$smoke_dir/restored.gdbm

gdbmtool "$database" store openeuler rva23
test "$(gdbmtool "$database" fetch openeuler)" = rva23
gdbm_dump "$database" "$dump_file"
gdbm_load "$dump_file" "$restored"
test "$(gdbmtool "$restored" fetch openeuler)" = rva23
