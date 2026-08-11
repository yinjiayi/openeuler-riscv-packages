#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- acl libacl libacl-devel

smoke_file=$(mktemp)
trap 'rm -f "$smoke_file"' EXIT

setfacl -m u::rw-,g::r--,o::--- "$smoke_file"
acl_text=$(getfacl --absolute-names --omit-header "$smoke_file")
grep -Fx 'user::rw-' <<<"$acl_text"
grep -Fx 'group::r--' <<<"$acl_text"
grep -Fx 'other::---' <<<"$acl_text"
