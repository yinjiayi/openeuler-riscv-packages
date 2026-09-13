#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- detox
test "$(detox -V)" = "detox 3.0.1"

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
touch "$smoke_dir/Foo Bar"
detox "$smoke_dir/Foo Bar"
test -f "$smoke_dir/Foo_Bar"

test "$(printf 'Foo Bar\n' | inline-detox)" = "Foo_Bar"
