#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- renameutils
for command in qcmd qmv qcp icmd imv icp deurlname; do
    "$command" --version >/dev/null
done

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
printf 'openEuler RVA23\n' >"$smoke_dir/name%20with%20spaces"
(cd "$smoke_dir" && deurlname 'name%20with%20spaces' && test -f 'name with spaces')
