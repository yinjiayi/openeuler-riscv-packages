#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail

lock_file=${1:-ci/image.lock}
[[ -f $lock_file ]] || { printf 'image lock not found: %s\n' "$lock_file" >&2; exit 2; }

value() {
  local key=$1
  sed -nE "s/^${key}:[[:space:]]*\"?([^\"]*)\"?[[:space:]]*$/\\1/p" "$lock_file"
}

image=$(value image)
digest=$(value digest)
[[ $image == ghcr.io/yinjiayi/openeuler-riscv64-rpmbuild ]] \
  || { printf 'unexpected locked image repository: %s\n' "$image" >&2; exit 2; }
[[ $digest =~ ^sha256:[0-9a-f]{64}$ ]] || {
  printf 'CI image is not published/locked yet; ci/image.lock needs a verified sha256 digest\n' >&2
  exit 3
}
printf '%s@%s\n' "$image" "$digest"

